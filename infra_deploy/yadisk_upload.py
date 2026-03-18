import glob
import os

import yadisk

# добавьте переменную окружения через терминал
token = os.environ.get("YADISK_TOKEN")
db_backup = glob.glob("postgres_backup*")[0]

y = yadisk.YaDisk(token=token)
# уточнить путь к папке с бэкапапми на яндекс диске
y.upload(db_backup, dst_path=f"/backups/{db_backup}")
