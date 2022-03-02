[![codestyle PEP8 and tests](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/codestyle_pep8_and_tests.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/codestyle_pep8_and_tests.yaml)
[![deploy](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/backend_deploy.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/backend_deploy.yaml)
[![python safety](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/check_vulnerabilities.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/check_vulnerabilities.yaml)

# Бэкенд "Любимовка"

## Что сделано и чем отличается от структуры по умолчанию
- poetry как менеджер пакетов и управления зависимостями
- изменена структура:
    - настройки и django приложения в папке config
    - папка для приложений: apps
- отдельные настройки для тестов или локального / prod окружения
- базовые линтеры (black, flake8)
- pre-commit хуки
- используется PostgreSQL
- базовая модель TimeStampedModel (импортировать из core.models)
- автодокументация swagger/redoc (http://base_url/api/v1/schema/swagger-ui/ или http://base_url/api/v1/schema/redoc/)

## Общие требования к стилю кода - [ссылка](docs/codestyle.md)

## Что нужно проверить, когда вы сделали PR - [чек-лист для PR](docs/pull_request.md)

## Правила работы с git (как делать коммиты и pull request-ы)
1. Две основные ветки: master и develop
2. Ветка develop — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. В master будет то, что будет заливаться на прод (CI/CD)
4. Порядок именования веток
    - весь новый функционал — **feature/название-функционала**
    - исправление ошибок — **bugfix/название-багфикса**
5. При создании новой ветки наследоваться от develop
6. PR в develop и master должны быть базово покрыты тестами:
    - на доступность эндпонтов
    - проверка списка полей
    - проверен критичный функционал (пример: фильтр по слову “сосиска” возвращает только результаты с “сосиска“)

Правила возможно будут добавляться и обновляться.
## Подготовка окружения для разработки

Что нужно подготовить предварительно:
1. **poetry** \
Зависимости и пакеты управляются через **poetry**. Детальное описание + как установить в [документации poetry](https://python-poetry.org/docs/cli/).
2. **Docker** \
Для разработки используется Postgres SQL. Базу данных удобно запускать через Docker.
3. Файлы **requirements** \
Файлы редактировать вручную не нужно. Обновляются через pre-commit хуки (если есть изменение в зависимостях, то список обновится при коммите).
4. **pre-commit хуки** \
[Документация](https://pre-commit.com)\
При каждом коммите выполняются хуки (автоматизации) перечисленные в **.pre-commit-config.yaml**. Если не понятно какая ошибка мешает сделать коммит можно запустить хуки вручную и посмотреть ошибки:
    ```shell
    pre-commit run --all-files
    ```

Если всё подготовлено:
1. Склонируйте проект, перейдите в папку backend
    ```shell
    git clone git@github.com:Studio-Yandex-Practicum/Lubimovka_backend.git
    cd Lubimovka_backend
    ```
2. Убедитесь что poetry установлен. Активируйте виртуальное окружение. Установите зависимости
    ```shell
    poetry shell
    poetry install
    ```
3. Установите pre-commit хуки
    ```shell
    pre-commit install --all
    ```
4. В IDE скорее всего потребуется указать путь до интерпретатора (скопируйте в IDE путь который вернет команда)
    ```shell
    poetry env info --path
    ```
5. Установить pre-commit хуки
    ```shell
    pre-commit install --all
    ```
6. Для запуска базы данных используйте postgres-local.yaml и docker-compose.
    ```
    docker-compose -f postgres-local.yaml up -d
    ```
7. Остановка, удаление и все остальные команды как с любым контейнером docker
    - Остановить контейнер с БД:
        ```shell
        docker-compose -f postgres-local.yaml down
        ```
    - Остановить контейнер с БД удалив данные:

        ```shell
        docker-compose -f postgres-local.yaml down --volumes
        ```
8.  Для корректной работы сервиса по выгрузке заявок (на участие в фестивале) в Google-таблицу потребуются переменные окружения - добавьте файл **.env** в корень папки проекта. Для проверки работы сервиса необходимо в админ панели внести spreadsheetId таблицы, в которую будет происходить выгрузка и наименование нужного листа. Не забудьте разрешить пользователю с адресом "lubimovka@swift-area-340613.iam.gserviceaccount.com" вносить изменения в вашу таблицу (Настройки доступа).
## Про тесты

Тестов нет, но есть настройки для ускорения тестов + настройки для запуска unittest через pytest (удобно в vscode)

## Права пользователей админ-зоны
Доступна команда для установки прав пользователей согласно их группам:
```
./ manage.py set_perms
```

## Заполнение БД тестовыми данными
Доступна команда для наполнения БД данными:
```
./ manage.py filldb
```
Команда сейчас немного "сырая". Но заполняет такими тестовыми данными, как:
- персоны
- партнёры
- попечители
- волонтёры
- команды фестиваля
- пользователи-админы и редакторы (для входа используем ник admin_X или editor_X, где Х - число от 1 до 5 и дефолтный пароль "pass")

Для создания таких тестовых данных, как проекты, новости и блог доступна команда:
```
./ manage.py filldb_articles
```
Ее следует применять ПОСЛЕ команды filldb (создает объекты, необходимые для создания сложных сущностей блога/проекта/новости).

Для очистки БД от данных (но не удаления таблиц) можно использовать команду:
```
./ manage.py flush
```
