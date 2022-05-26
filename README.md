# api_final
### Описание
Блог для тех кто хочет высказать свое мнение, но через api.
### Технологии
- Python 3.7
- Django 2.2.16
- Djangorestframework 3.12.4
- Google
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
### Примеры запросов
- GET /api/v1/posts/?offset=300&limit=100",
> <font color="green">200</font>
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
- POST /api/v1/follow/
```json
{
  "following": "string"
}
```
> <font color="blue">201</font>
```json
{
"user": "string",
"following": "string"
}
```
- PUT /api/v1/posts/{post_id}/comments/{id}/
```json
{
  "text": "string"
}
```
> <font color="pink">200</font>
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2022-05-24T14:15:22Z",
  "post": 0
}
```
### Авторы
Митрошин Алексей