import os
import pathlib
import shutil
import time
from logging.handlers import TimedRotatingFileHandler


class TimedRotatingFileHandlerWithZip(TimedRotatingFileHandler):
    """
    Override TimedRotatingFileHandler for move old logs to path - /old/.

    In doRollover -do a rollover; in this case, a date/time stamp is appended to the filename
    when the rollover happens. And also checks and executes backupCount and oldbackupCount.

    backupCount - the number of logs in quick access.
    oldbackupCount - the number of logs to be stored in the old folder.
    If they are greater than this value, the old ones are deleted.
    """

    def __init__(self, filename, when, interval, backupCount, oldbackupCount):

        pathlib.Path(filename).parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=str(filename),
            when=str(when),
            interval=int(interval),
            backupCount=int(backupCount),
        )
        self.oldbackupCount = int(oldbackupCount)

    def getFilesToMoving(self):
        dir_name = self.file_path.parent
        base_name = self.baseFilename
        filenames_in_dir = os.listdir(dir_name)

        result = []

        ending = self.file_path.suffix
        prefix = self.file_path.stem + "_"
        prefix_len = len(prefix)

        for filename in filenames_in_dir:
            # Our files could be just about anything after custom naming, but
            # likely candidates are of the form
            # foo.log.DATETIME_SUFFIX or foo.DATETIME_SUFFIX.log
            if (
                not filename.startswith(base_name)
                and filename.endswith(ending)
                and len(filename) > (prefix_len + 1)
                and not filename[prefix_len + 1].isdigit()
            ):
                continue

            if filename[:prefix_len] == prefix:
                suffix = filename[prefix_len:]
                parts = suffix.split(".")
                for part in parts:
                    if self.extMatch.match(part):
                        result.append(str(pathlib.PurePath.joinpath(dir_name, filename)))
                        break
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[: len(result) - self.backupCount]
        return result

    def getFilesToDelete(self):
        old_logs = os.listdir(self.old_logs_directory)
        if len(old_logs) > self.oldbackupCount:
            logs_to_delete = sorted(old_logs)[: len(old_logs) - self.oldbackupCount]
            for old_log in logs_to_delete:
                old_log_path = self.old_logs_directory + old_log
                os.remove(old_log_path)

    @property
    def file_path(self):
        return pathlib.Path(self.baseFilename)

    @property
    def old_logs_directory(self):
        path = str(self.file_path.parent) + "/old/"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def doRollover(self):  # Noqa
        if self.stream:
            self.stream.close()
            self.stream = None

        currentTime = int(time.time())  # Get the time that this sequence started at and make it a TimeTuple.
        dstNow = time.localtime(currentTime)[-1]
        time_point = self.rolloverAt - self.interval
        timeTuple = time.localtime(time_point)
        dstThen = timeTuple[-1]
        if dstNow != dstThen:
            if dstNow:
                addend = 3600
            else:
                addend = -3600
            timeTuple = time.localtime(time_point + addend)

        rotation_file_name = self.rotation_filename(
            str(self.file_path.parent)
            + "/"
            + self.file_path.stem
            + "_"
            + time.strftime(self.suffix, timeTuple)
            + self.file_path.suffix
        )
        if pathlib.Path(rotation_file_name).exists():
            os.remove(rotation_file_name)
        self.rotate(self.baseFilename, rotation_file_name)

        for file_path in self.getFilesToMoving():  # Moving old log files to the old's path.
            filename = file_path.split("/")[-1]
            new_file_path = self.old_logs_directory + filename
            shutil.move(file_path, new_file_path)

        self.getFilesToDelete()  # Delete the oldest log files in the old's path.

        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        # If DST changes and midnight or weekly rollover, adjust for this.
        if self.when == "MIDNIGHT" or self.when.startswith("W"):
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600  # DST kicks in before next rollover, so we need to deduct an hour
                else:
                    addend = 3600  # DST bows out before next rollover, so we need to add an hour
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
