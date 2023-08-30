# Foodgram

 Foodgram Assistant is an online service and API for it. On this service, users will be able to publish recipes, subscribe to other users' publications, add favorite recipes to the "Favorites" list, and download a consolidated list of products needed to prepare one or more selected dishes before going to the store.

## About the project 

- The project is wrapped in Docker containers;
- The project is deployed on a server http://51.250.17.104/
  
## Technologies
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker

## Dependencies
- Listed in the file backend/requirements.txt


## To launch on your own server

1. Install `docker` and `docker-compose` on the server
2. Create the file `/infra/.env` The template for filling the file is located in `/infra/.env.example`.
3. From the `/infra/` directory, run the `docker-compose up -d --build` command
5. Perform migrations `docker-compose exec -it web python manage.py migrate`
6. Create a superuser `docker-compose exec -it web python manage.py createsuperuser`
7. Collect static files `docker-compose exec web python manage.py collectstatic --no-input`

8. Documentation for the API is available at: <http://localhost/api/docs/redoc.html>.

## Author

Vladimir Maksimov

## Admin login details

Email address: admin@yandex.ru
Login: Admin1
Password: Ad123123Min
