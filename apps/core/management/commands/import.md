Команды import_blogs и import_news предназначены для добавления на сайт блогов и новостей со старого сайта. Команды должны применяться однократно. Добавляемые материалы отмечаются как созданные пользователем "Архивариус". При запуске команды записи пользователя "Архивариус" предварительно удаляются удаляются, поэтому многократный вызов команд не приводит к дублированию записей.

**Команды для выполнения на сервере при импорте блогов и новостей**
```shell
ssh developer@stage.dev.lubimovka.ru
developer@lubimovka-stage:~$ mkdir import
developer@lubimovka-stage:~$ cd import
developer@lubimovka-stage:~/import$ wget https://storage.yandexcloud.net/lubimovka/blog_dump2.zip
developer@lubimovka-stage:~/import$ wget https://storage.yandexcloud.net/lubimovka/images_dump2.zip
developer@lubimovka-stage:~/import$ wget https://storage.yandexcloud.net/lubimovka/news_dump2.zip
developer@lubimovka-stage:~/import$ unzip images_dump2.zip
developer@lubimovka-stage:~/import$ unzip blog_dump2.zip
developer@lubimovka-stage:~/import$ unzip news_dump2.zip
developer@lubimovka-stage:~$ sudo docker cp import containerid:/code
developer@lubimovka-stage:~$ sudo docker exec -it containerid bash
root@containerid:/code# python manage.py import_blogs import/j_content_blogs_202301281813.json /code/import/
root@containerid:/code# python manage.py import_news import/j_content_news_202302030259.json /code/import/
```

Примечания:
- developer@stage.dev.lubimovka.ru - имя пользователя и домен, на котором запущена серверная часть
- containerid - номер docker-контейнера серверной части
