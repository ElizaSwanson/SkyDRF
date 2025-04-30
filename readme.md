## **Зависимости:**

Docker (должен быть установлен и запущен Docker Desktop)
Docker Compose

## **Установка:**

1. Клонируйте репозиторий:
https://github.com/ElizaSwanson/SkyDRF.git

2. Создайте и заполните файл `.env`, ориентир - файл `.env.example`
3. Выполните команду запуска: `docker-compose up --build`
4. Примените миграции путем выполнения команды `python manage.py migrate`.
5. Откройте новый терминал и выполните:
`docker-compose exec web python manage.py migrate`
6. Создайте суперпользователя (опционально):
`docker-compose exec web python manage.py createsuperuser`, далее следуйте инструкциям. 
7. Вы справились, проект доступен по адресу: http://localhost:8000/
8. Для остановки контейнера выполните: ``docker-compose down``

## Хоткеи: 

Проверить работоспособность контейнеров -  `docker-compose ps`
Посмотреть все имеющиеся функции, модели итд - http://localhost:8000/redoc/