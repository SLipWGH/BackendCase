# Тестовое задание на позицию инженера по автоматизации

## Стартовые настройки

Далее приведена инструкция для локального запуска проекта.

1. Подготовка виртуального окружения

Зайдите в директорию `backend/` и создайте виртуальное окружение:

`python -m venv venv`

Далее в директории `backend` и активируйте виртуальное окружение:

`source venv/bin/activate`

Установите зависимости:

`pip install -r requirements.txt`


Виртуальное окружение готово

1. команда `make up` поднимает докер-контейнер с базой данных.

Теперь, когда база данных готова, нужно накатить необходимые таблицы. Сделаем это с помощью пакета для контроля миграций `alembic`. Нужно удалить все миграции из каталога `backend/migrations/versions` и выполнить в каталоге `backend` команды (создание миграции и ее применение):

`alembic revision --autogenerate`

`alembic upgrade +1`

Осталось только инициализировать базу начальными данными. Для этого нужно подключиться к базе данных :

`psql -h 127.0.0.1 -p 5432 -U postgres -d postgres` (потребуется ввести пароль `postgres`)

Далее нужно выполнить скрипт инциализации `init_db.sql`:

`database=> \i {путь до проекта}/backend/src/init_db.sql;`

Если в консоли только логи от `INSERT`, то все готово.

1. Старт приложения

Перейдите в директорию `backend/src/` и выполните команду:

`uvicorn app.app:app --reload`.

После этого сервер должен запуститься. API можно посмотреть и потестировать в swagger "http://127.0.0.1:8000/docs"
