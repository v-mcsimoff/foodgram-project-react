# Foodgram

 Продуктовый помощник - это онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## О проекте 

- Проект завернут в Docker-контейнерах;
- Проект развернут на сервере http://51.250.17.104/
  
## Стек технологий
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker

## Зависимости
- Перечислены в файле backend/requirements.txt


## Для запуска на собственном сервере

1. Установите на сервере `docker` и `docker-compose`
2. Создайте файл `/infra/.env` Шаблон для заполнения файла нахоится в `/infra/.env.example`
3. Из директории `/infra/` выполните команду `docker-compose up -d --build`
5. Выполните миграции `docker-compose exec -it backend python manage.py migrate`
6. Создайте Администратора `docker-compose exec -it backend python manage.py createsuperuser`
7. Соберите статику `docker-compose exec backend python manage.py collectstatic --no-input`

8. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.

## Автор

Владимир Максимов

## Данные для входа в админку

Email address: admin@yandex.ru
Password: Ad123123Min