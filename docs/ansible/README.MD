# Подготовка сервера к развертыванию проекта

Это руководство предназначено для первоначальной настройки виртуальной машины для использования в качестве тестового сервера проекта Любимовка. Приложенная к настоящему руководству [книга сценариев](playbook.yaml) Ansible рассчитана на работу с сервером под управлением Ubuntu 22.04. Некоторые сценарии, в частности зависящие от Polkit, могут не работать на других версиях операционной системы.

Для работы вам нужна учетная запись пользователя с правом повышения привелегий (sudo) на сервере и возможностью подключения по протоколу SSH с помощью ключа.

## Установка Ansible

Ansible можно запустить только на машине под управлением Linux или Windows WSL. Подрообности можно узнать в [руководстве](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements) по установке Ansible.

Создайте виртуальное окружение и установите в него Ansible.
```bash
python3 -m venv venv
source venv/bin/activate
pip install ansible
```
## Проверка работоспособности

Проверьте правильность адреса сервера в [реестре](inventory.yaml).

Проверка реестра обслуживаемых машин

```bash
ansible-inventory -i inventory.yaml --list
```

Опрос состояния машин реестра

```bash
ansible lubimovka -m ping -i inventory.yaml
```
или
```bash
ansible all -m ping -i inventory.yaml
```

Если при опросе машин возникли ошибки, убедитесь в правильности имени (IP-адреса) в реестре и работоспособности подключения к серверу.

## Запуск сценария подготовки сервера

Запустите книгу сценариев для подготовки сервера (установка Docker, сетевого экрана, подготовка среды к развертыванию проекта).

После запуска будет предложено ввести пароль `BECOME` для повышения привелегий (sudo). Если для вашей учетной записи пароль не требуется, можно ввести пустой пароль или удалить ключ `--ask-become-pass` из команды.

```bash
ansible-playbook --ask-become-pass -i inventory.yaml playbook.yaml
```

Если имя пользователя на локальной машине не совпадает с именем пользователя на сервере, укажите последнее при запуске книги сценариев:
```bash
ansible-playbook --ask-become-pass --user <username> -i inventory.yaml playbook.yaml
```


## Подготовка системы развертывания GitHub

В секрете Github под именем `HOST` задайте имя сервера (на момент написания инструкции `stage.dev.lublimovka.ru`).
В секрете Github под именем `USERNAME` задайте `github`.

В результате работы сценария на локальной машине в папке `key` будет получен приватный ключ машины, которой разрешен доступ к серверу. Его нужно поместить в секрет Github под именем `SSH_PRIVATE_KEY` среды `stage` или `test`, а с локальной машины полностью удалить.

В секрет Github под именем `SSH_KNOWN_HOSTS` нужно поместить электронную подпись (fingerprint) виртуальной машины. Её можно найти в файле `known_hosts` на машине, с которой вы подключались к серверу. В начале подписи имя или IP-адрес сервера должны совпадать с указанным в секрете `HOST`.
Пример электронной подписи сайта:
```
stage.dev.lubimovka.ru ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCSwnogrjphZAEaBZtK4HrkO2Y7VuDBuWvibLSXgVR0o/d7SrNSaj9TFbAhkKBQAhZ8TH9MCbr9D54HSoj0Drv0ihIe+2RYkEK10bMrllc42EIycSCiXhEi2T4lrvOBx/QOxUJYv0J8GnakI/v/TkMVQRXmzxT/apZtElc6VsMcVsuMUf1WcHxzb5NBrdCIaQbA0uh5yFotLw9TZgXMomjEcjNTb+rcbNDcppqJ34M+m2Wr825A6s+O6PU2hwm1TDTNFseeQ/HNnjtic/kT/OWql1q2NABZXoJUvrMe5UYa4EkTyPaM9R/cbSBJeub+Z2r7eqEWqlJCgrPsyXLZz5hLw2Ufa6nB8YYNdkoZaAlR1ZxY8RON4nSSWbFVJTCkElcebnc8nCRXPNAZZZ4fQ+LObC+H87/1XwlnKZndd7HYYNo5hYE2ZzEPrDdhw3LiaaSjdqC6nv/sDRH6NfLcdxTttlFM82tUFqMRMo/hS9ejH3BxLfxhUIIZVla0ad6izGU=
```

## Проверка развертывания

Запустите GitHub Action развертывания проекта. Проверьте, что развертывание завершилось успешно и сервер доступен в Интернет.
В случае успеха, можно удалить Ansible с локальной машины.
