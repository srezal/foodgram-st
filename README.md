# Запуск

1) Склонируйте репозиторий, выполнив команду 
```
git clone git@github.com:srezal/foodgram-st.git
```
2) Создайте в поддиректории infra файл .env на основе .env.example, файл должен содержать следующие значения
```
DB_NAME=name
DB_USER=user
DB_PASSWORD=password
DB_HOST=db_host
DB_PORT=db_port
SECRET_KEY=secret_key
```
3) В этой же директории выполните команду
```
docker compose up
```

## Импорт данных

Для импорта данных необходимо выполнить следующую команду

```
docker exec -it foodgram-backend python manage.py loaddata ./data/db.json
```

Приложение доступно по ссылке http://localhost

Панель администратора доступна по ссылке http://localhost/admin (email: admin.user@example.com, пароль: 123)

Справка по API доступна по ссылке  http://localhost/api/docs/


# Стек технологий

* Backend: Django + DRF

* Frontend: React

* База данных: PostgreSQL

* Контейнеризация: Docker

* Документация API: Swagger/Redoc


# Автор

Ринг Сергей

telegram: @srezall