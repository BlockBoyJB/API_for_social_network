# API for social network v2.0
# Documentation

#### функционал api:
- Создает пользователя (проверяет почту на правильность), который может писать посты, ставить реакции (heart, like, dislike, boom, ...) на посты других пользователей.
Также после создания на указанную почту приходит письмо с кодом подтверждения. Пользователь с неподтвержденной почтой не может создавать посты
- Выдает данные по конкретному пользователю
- Удаляет пользователя
- Создает пост
- Выдает данные по конкретному посту
- Удаляет пост
- Пользователь ставит реакцию на пост
- Выдает все посты пользователя, отсортированные по количеству реакций
- Генерирует список пользователей, отсортированный по количеству реакций
- Генерирует график пользователей по количеству реакций


### usage examples

- **Создание пользователя:**
`POST /users/create`
###### request:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "username": "string"
}
```
###### response:
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": 0,
  "posts": [],
  "user_id": "string",
  "status": "unconfirmed",
  "message": "check_your_email"
}
```

- **Получение данных о конкретном пользователе**
`GET /users/user`

###### request:
```json
{
  "username": "string"
}
```
or
```json
{
  "user_id": "string"
}
```

###### response:
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number",
  "status": "number",
  "uuid": "string"
}
```

- **Подтверждение почты пользователя**
`POST /users/user/verify`

###### request:
```json
{
  "username": "string",
  "code": "string"
}
```

###### response:
```json
{
  "message": "user with username {username} successfully confirmed"
}
```

- **Удаление пользователя**
`DELETE /users/user/delete`

###### request:
```json
{
  "user_id": "string"
}
```
or 
```json
{
  "username": "string"
}
```

###### response:
```json
{
  "message": "post deleted successfully"
}
```

- **Создание поста** 
`POST /posts/create`

###### request:
```json
{
  "username": "string",
  "title": "string",
  "text": "string"
}
```

###### response:
```json
{
  "title": "string",
  "username": "string",
  "reactions": [],
  "text": "string"
}
```

- **Получение данных по определенному посту** 
`GET /posts/post`

###### request:
```json
{
  "username": "string",
  "title": "string"
}
```
or
```json
{
  "post_id": "string"
}
```

###### response:
```json
{
  "title": "string",
  "author_username": "string",
  "post_id": "string",
  "text": "string",
  "reactions": [
    "string",
    "string",
    "other_reactions..."
  ]
}
```

- **Удаление постов пользователя**
`DELETE /posts/post/delete`

###### request:
```json
{
  "post_id": "string"
}
```
or
```json
{
  "title": "string",
  "username": "string"
}
```

###### response:
```json
{
  "message": "post deleted successfully"
}
```


- **Поставить реакцию посту** 
`POST /posts/post/reaction`

###### request:
```json
{
  "reaction": "string",
  "username": "string",
  "title": "string"
}
```
or
```json
{
  "reaction": "string",
  "post_id": "string"
}
```

###### response
```
{}
```

- **Получение всех постов пользователя, отсортированных по количеству реакций** 
`GET /users/user/posts`

`asc` обозначет `ascending` (по возрастанию)<br>
`desc` обозначет `descending` (по убыванию)

###### request:
```json
{
  "sort": "asc/desc",
  "username": "string"
}
```
or
```json
{
  "sort": "asc/desc",
  "user_id": "string"
}
```

###### response:
```json
{
	"posts": [
    	{
  			"username": "string",
  			"title": "string",
  			"post_id": "string",
            "text": "string",
  			"reactions": [
  				"string",
    			"other_reactions..."
  			] 
  		},
        {
        	"other_posts": "..."
        }
    ]
}
```

- **Получение всех пользователей, отсортированных по количеству реакций** 
`GET /users/leaderboard`

`asc` обозначет `ascending` (по возрастанию)<br>
`desc` обозначет `descending` (по убыванию)

###### request:
```json
{
  "type": "list",
  "sort": "asc/desc"
}
```

###### response:
```json
{
	"users": [
    	"1 - {username}, reactions - {num of reactions}",
        "2 - ..."
    ]
}
```

- **Получение графика пользователей по количеству реакций** 
`GET /users/leaderboard` (также можно указать тип сортировки)


###### request:
```json
{
  "type": "graph",
  "sort": "asc/desc"
}
```

###### response:
```html
<img src="leaderboard.png">
```