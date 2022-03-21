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
        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        super().__init__(
            filename=str(filename),
            when=str(when),
            interval=int(interval),
            backupCount=int(backupCount),
        )
        self.oldbackupCount = oldbackupCount

    def getFilesToMoving(self):
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []

        name, ending = os.path.splitext(baseName)
        prefix = name + "."
        plen = len(prefix)
        for fileName in fileNames:
            if self.namer is None:
                if not fileName.startswith(baseName):
                    continue
            else:
                if (
                    not fileName.startswith(baseName)
                    and fileName.endswith(ending)
                    and len(fileName) > (plen + 1)
                    and not fileName[plen + 1].isdigit()
                ):
                    continue

            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                parts = suffix.split(".")
                for part in parts:
                    if self.extMatch.match(part):
                        result.append(os.path.join(dirName, fileName))
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
    def logs_directory(self):
        return str(pathlib.Path(self.baseFilename).parent)

    @property
    def old_logs_directory(self):
        path = self.logs_directory + "/old/"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def doRollover(self):  # Noqa
        if self.stream:
            self.stream.close()
            self.stream = None

        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        time_point = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(time_point)
        else:
            timeTuple = time.localtime(time_point)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(time_point + addend)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, timeTuple))
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)

        if self.backupCount > 0:
            for file_path in self.getFilesToMoving():
                filename = file_path.split("/")[-1]
                new_file_path = self.old_logs_directory + filename
                shutil.move(file_path, new_file_path)

        if self.oldbackupCount > 0:
            self.getFilesToDelete()

        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        if (self.when == "MIDNIGHT" or self.when.startswith("W")) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
