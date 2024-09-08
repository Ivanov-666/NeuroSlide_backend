# NeuroSlide

## Подготовка к запуску и запуск проекта

### Если используете virtualenv:

Создать окружение

```
python -m venv .venv
```

Активировать

```
./.venv/Scripts/activate
```

Установить зависимости

```
   make install
```

Запустить проект

```
   make start_service
```

### Если используете conda:

Создать окружение

```
make env
```

Активировать

```
conda activate neuroslide
```

Установить зависимости

```
   make install
```

Запустить проект

```
   make start_service
```

Также для работы понадобится .env файл, в котором будет находится IAM Token для YandexGpt и настроки для подключения к redis название полей см. в settings.py

## pre-commit

Установка

```bash
$ pip install pre-commit
```

Добавления хуков в .git

```bash
$ pre-commit install
```

При выполнении команды `git commit` будут выполняться проверки
на форматирование файлов, кода и тд (подробнее о
хуках в .pre-commit-config.yaml).

*Если какая-то проверка не была пройдена, необходимо
повторить команды `git add` и `git commit`*

Если были сделаны коммиты до установки pre-commit:

```bash
$ pre-commit run --all-files
```

Эта команда отформатирует все файлы в директории.

## Redis

   Установка на linux:

```bash
$ sudo apt install redis-server
```

   Запуск:

```bash
sudo systemctl start redis.service
```
