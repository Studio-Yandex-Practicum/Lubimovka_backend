import gzip
import os
import pathlib
import shutil
from logging.handlers import TimedRotatingFileHandler


class TimedRotatingFileHandlerWithZip(TimedRotatingFileHandler):
    """Override TimedRotatingFileHandler and add compress with gzip."""

    def __init__(self, filename, when, interval, backupCount):
        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        super().__init__(
            filename=str(filename),
            when=str(when),
            interval=int(interval),
            backupCount=int(backupCount),
        )

    def doRollover(self):
        super().doRollover()
        log_path = pathlib.Path(self.baseFilename)
        log_directory = log_path.parent
        log_filename = log_path.stem
        files_in_directory = os.listdir(log_directory)
        log_file_prefix = (".gz", ".log")
        to_compress_list = []

        for log_file_to_compress in files_in_directory:
            if log_file_to_compress.startswith(log_filename) and not log_file_to_compress.endswith(log_file_prefix):
                to_compress_list.append(os.path.join(log_directory, log_file_to_compress))

        for log_file in to_compress_list:
            if pathlib.Path(log_file).exists():
                with open(log_file, "rb") as _old, gzip.open(log_file + ".gz", "wb") as _new:
                    shutil.copyfileobj(_old, _new)
                os.remove(log_file)
