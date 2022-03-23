# Проект 'Invites' - тестовое задание
---
### Описание
Проект - результат работы по тестовому заданию. REST API сервис реализованный на Django Rest Framework. Представляет собой реферальную систему.
Возможна авторизация по номеру телефона. Ввод пригласительного кода. 
Проект можно развернуть локально.
### Команда для клонирования репозитория 
    git clone https://github.com/timelord78/invites.git invites
### Создание виртуальной среды и установка зависимостей
    python -m venv venv
    pip install -r --requirements.txt
### Необходимо создать и заполнить файл .env (данные для БД Postgres)
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=localhost
### Запустить контейнер с БД PostgreSQL
    docker-compose up
### Выполнить миграции и создать суперпользователя и запустить сервер Django
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
### Наполнить тестовыми данными
 - через админ панель
 - через запросы к API
### Документация к проекту будет доступна по адресу:
    http://127.0.0.1:8000/redoc/
    


