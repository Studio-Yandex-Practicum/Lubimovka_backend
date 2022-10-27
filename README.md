[![Tests](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/pytests.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/pytests.yaml)
[![Prod build and deploy](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/backend_deploy_prod.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/backend_deploy_prod.yaml)
[![Stage build and deploy](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/backend_deploy_stage.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/backend_deploy_stage.yaml)
[![python safety](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/check_vulnerabilities.yaml/badge.svg)](https://github.com/Studio-Yandex-Practicum/Lubimovka_backend/actions/workflows/check_vulnerabilities.yaml)

# Бэкенд "Любимовка"

## Что сделано и чем отличается от структуры по умолчанию
- poetry как менеджер пакетов и управления зависимостями
- изменена структура:
    - настройки и django приложения в папке `/config`
    - папка для приложений: `/apps`
- отдельные настройки для тестов или локального / prod окружения
- базовые линтеры (black, flake8)
- pre-commit хуки
- используется PostgreSQL
- базовая модель `TimeStampedModel` (импортировать из `core.models`)
- автодокументация swagger/redoc (http://base_url/api/v1/schema/swagger-ui/ или http://base_url/api/v1/schema/redoc/)

## Общие требования к стилю кода - [ссылка](docs/codestyle.md)

## Что нужно проверить, когда вы сделали PR - [чек-лист для PR](docs/pull_request.md)

## Правила работы с git (как делать коммиты и pull request-ы)
1. Две основные ветки: `master` и `develop`
2. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. Создавая новую ветку, наследуйтесь от ветки `develop`
4. В `master` находится только production-ready код (CI/CD)
5. Правила именования веток
    - весь новый функционал — `feature/название-функционала`
    - исправление ошибок — `bugfix/название-багфикса`
6. PR в `develop` и `master` должны быть базово покрыты тестами:
    - на доступность эндпойнтов
    - проверка списка полей
    - проверен критичный функционал (пример: фильтр по слову “сосиска” возвращает только результаты с “сосиска“)


## Важные практики

### Создание миграций:
- При создании миграций данных "вручную" **обязательно** передавайте параметр reverse_code. Это необходимо для возможности откатывать миграции. Если при откате миграции данные изменять не требуется, в качестве значения можно использовать `RunPython.noop`. \
Пример:
```
# Ваш код
...
operations = [
    migrations.RunPython(your_command, reverse_code=migrations.RunPython.noop),
]
```

## Подготовка окружения для разработки

### Предварительные требования:
1. **Poetry** \
Зависимости и пакеты управляются через **poetry**. Убедитесь, что **poetry** [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/cli/).
2. **Docker** \
В проекте используется PostgreSQL. Рекомендуем запускать БД через Docker, следуя дальнейшим инструкциям.
3. Файлы **requirements** \
Файлы редактировать вручную не нужно. Обновляются через pre-commit хуки (если есть изменение в зависимостях, то список обновится при коммите).
4. **pre-commit хуки** \
[Документация](https://pre-commit.com)\
При каждом коммите выполняются хуки (автоматизации) перечисленные в **.pre-commit-config.yaml**. Если не понятно какая ошибка мешает сделать коммит можно запустить хуки вручную и посмотреть ошибки:
    ```shell
    pre-commit run --all-files
    ```

### Разворачиваем проект локально:
1. Склонируйте проект, перейдите в папку `/backend`
    ```shell
    git clone git@github.com:Studio-Yandex-Practicum/Lubimovka_backend.git
    cd Lubimovka_backend
    ```
2. Убедитесь что poetry установлен. Активируйте виртуальное окружение. Установите зависимости
    ```shell
    poetry shell
    poetry install
    ```
3. Сделайте миграции
    ```
    python manage.py migrate
    ```
4. Установите pre-commit хуки
    ```shell
    pre-commit install --all
    ```
5. Убедитесь, что при запуске ваш IDE использует правильное виртуальное окружение. В противном случае - самостоятельно укажите путь к виртуальному окружению. Посмотреть путь можно следующей командой:
    ```shell
    poetry env info --path
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
8. Файл `.env` должен находиться в корневой папке проекта. Если вы решите не создавать свой `.env` файл - в проекте предусмотрен файл `.env_local`, обеспечивающий переменные для базовой работы на локальном уровне.
9. Для корректной работы сервиса по выгрузке заявок (на участие в фестивале) в Google-таблицу потребуются переменные окружения - добавьте файл **.env** в корень папки проекта. Для проверки работы сервиса необходимо в админ панели внести `spreadsheetId` таблицы, в которую будет происходить выгрузка и наименование нужного листа. Не забудьте разрешить пользователю с адресом "lubimovka@swift-area-340613.iam.gserviceaccount.com" вносить изменения в вашу таблицу (Настройки доступа).
## Про тесты

Тестов нет, но есть настройки для ускорения тестов + настройки для запуска `unittest` через `pytest` (удобно в vscode)

## Права пользователей админ-зоны
Доступна команда для установки прав пользователей согласно их группам:
```
python manage.py set_perms
```

## Заполнение БД тестовыми данными
Доступна команда для наполнения БД данными:
```
python manage.py filldb
```
Команда заполняет базу такими тестовыми данными, как:
- персоны
- фестивали, пресс-релизы, волонтёры, команда фестиваля, попечители, партнёры, отборщики, площадки
- программы, авторы, пьесы
- спектакли, мастер-классы, читки, события
- баннеры, заявки на участие
- пользователи-админы, редакторы, журналисты и наблюдатели (для входа используем: admin_X (где Х - в диапазоне от 00 до 04), editor_X (где Х - в диапазоне от 05 до 09), journalist_X (X в диапазоне от 10 до 14), observer_X (где Х - в диапазоне от 15 до 16) и дефолтный пароль "pass"), пользователь суперадмин (superadmin/superadmin)

Для создания таких тестовых данных, как проекты, новости и блог доступна команда:
```
python manage.py filldb_articles
```
Ее следует применять ПОСЛЕ команды `filldb` (создает объекты, необходимые для создания сложных сущностей блога/проекта/новости).

Для очистки БД от данных (но не удаления таблиц) можно использовать команду:
```
python manage.py flush
```
