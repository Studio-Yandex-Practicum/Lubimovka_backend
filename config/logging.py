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
        log_dir = os.path.dirname(self.baseFilename)
        to_compress = [
            os.path.join(log_dir, log_file)
            for log_file in os.listdir(log_dir)
            if log_file.startswith(os.path.basename(os.path.splitext(self.baseFilename)[0]))
            and not log_file.endswith((".gz", ".log"))
        ]
        for log_file in to_compress:
            if os.path.exists(log_file):
                with open(log_file, "rb") as _old, gzip.open(log_file + ".gz", "wb") as _new:
                    shutil.copyfileobj(_old, _new)
                os.remove(log_file)
