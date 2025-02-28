# Микросервис для скачивания файлов

Микросервис помогает работе основного сайта, сделанного на CMS и обслуживает
запросы на скачивание архивов с файлами. Микросервис не умеет ничего, кроме упаковки файлов
в архив. Закачиваются файлы на сервер через FTP или админку CMS.

Создание архива происходит на лету по запросу от пользователя. Архив не сохраняется на диске, вместо этого по мере упаковки он сразу отправляется пользователю на скачивание.

От неавторизованного доступа архив защищен хешом в адресе ссылки на скачивание, например: `http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/`. Хеш задается названием каталога с файлами, выглядит структура каталога так:

```
- photos
    - 3bea29ccabbbf64bdebcc055319c5745
      - 1.jpg
      - 2.jpg
      - 3.jpg
    - af1ad8c76fda2e48ea9aed2937e972ea
      - 1.jpg
      - 2.jpg
```


## Как установить

Для работы микросервиса нужен Poetry и Python версии не ниже 3.6.

```bash
cd app && poetry install
poetry shell
```

## Как запустить

```bash
python server.py
```
### Для вызова справки
```bash
python server.py -h
```

Сервер запустится на порту 8080, чтобы проверить его работу перейдите в браузере на страницу [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Как развернуть на сервере
Для запуска проекта на сервере в директории `./app` нужно создать `.env` файл и записать в него следующие переменные:
```dotenv
LOGGING_LEVEL=10
STORAGE_DIR="/test_photos"
```
Переменная `LOGGING_LEVEL` отвечает за наличие логгирования и его уровень. Возможные значения:

|  LOGGING_LEVEL  |   STATUS   |
|:---------------:|:----------:|
|        0        |   NOTSET   |
|       10        |   DEBUG    |
|       20        |    INFO    |
|       30        |  WARNING   |
|       40        |   ERROR    |
|       50        |  CRITICAL  |
|       100       |  DISABLE   |

Подробнее про логгирование: [https://docs.python.org/3/library/logging.html#logging-levels](https://docs.python.org/3/library/logging.html#logging-levels)

Переменная `STORAGE_DIR` описывает относительный путь к директрории, где будут храниться данные для скачивания. В репозитории присутствует директория `test_photos`, в которой размещены файлы для тестирования приложения.
### Запуск Docker-compose
В корневой директории выполнить следующую команду:
```bash
docker-compose up --build
```

После этого перенаправить на микросервис запросы, начинающиеся с `/archive/`. Например:

```
GET http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/
GET http://host.ru/archive/af1ad8c76fda2e48ea9aed2937e972ea/
```

# Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).