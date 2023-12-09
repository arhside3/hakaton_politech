Автор:
- @arhside3
Контакты:
[Крещенский Богдан](https://t.me/arhside3)

Foodgram - это проект в котором можно создавать рецепты, редактировать их, а также подписываться на автора рецепта и добавлять рецепты в избранное, и в корзину

Техно-стек:
- nginx 
- javascript 
- python 
- django 
- djangorest 
- postgres 
- docker

Как запустить проект на локальной машине с помощью Docker
- Клонирование репозитория
```
git clone git@github.com:arhside3/foodgram-project-react.git - типо он есть
```
- В корневой папке проекта вызовите команду Docker compose up
```
docker compose up
```
- Выполните миграцию базы данных в запущенном контейнере бэкенда
```
docker compose exec backend python manage.py migrate
```
- Сбор статических файлов для панели администратора Django
```
docker compose exec backend python manage.py collectstatic
```
- Скопируйте эти файлы в целевую папку, связанную с томом Docker
```
docker compose exec backend cp -r /app/collected_static/. /static/
```


Импорт CSV файлов на локальном сервере
- ингридиенты
```
docker-compose exec backend python manage.py import_ingredients 
```
- тэги
```
docker-compose exec backend python manage.py import_tags 
```