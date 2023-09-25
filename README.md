# API_for_social_network v1.0
# Documentation
###### Используемый фреймворк - flask 2.3.3

#### тз:
- Создает пользователя (проверяет почту на правильность), который может писать посты, ставить реакции (heart, like, dislike, boom, ...) на посты других пользователей
- Выдает данные по конкретному пользователю
- Создает пост
- Выдает данные по конкретному посту
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
  "email": "string"
}
```
###### response:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number",
  "posts": []
}
```

- **Получение данных о конкретном пользователе**
`GET /users/<user_id>`
###### response:
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "total_reactions": "number",
  "posts": [
    "number",
    ...
  ]
}
```

- **Создание поста** 
`POST /posts/create`

###### request:
```json
{
  "author_id": "number",
  "text": "string"
}
```

###### response:
```json
{
  "id": "number",
  "author_id": "number",
  "text": "string",
  "reactions": [
  	"string",
    ...
  ] 
}
```

- **Получение данных по определенному посту** 
`GET /posts/<post_id>`

###### response:
```json
{
  "id": "number",
  "author_id": "number",
  "text": "string",
  "reactions": [
  	"string",
    ...
  ] 
}
```

- **Поставить реакцию посту** 
`POST /posts/<post_id>/reaction`

###### request:
```json
{
  "reaction": "string"
}
```

###### response
```
{}
```

- **Получение всех постов пользователя, отсортированных по количеству реакций** 
`GET /users/<user_id>/posts`

`asc` обозначет `ascending` (по возрастанию)<br>
`desc` обозначет `descending` (по убыванию)

###### request:
```json
{
  "sort": "asc/desc"
}
```

###### response:
```json
{
	"posts": [
    	{
  			"id": "number",
  			"author_id": "string",
  			"text": "string",
  			"reactions": [
  				"string",
    			...
  			] 
  		},
        {
        	...
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
    	{
          "id": "number",
          "first_name": "string",
          "last_name": "string",
          "email": "string",
          "total_reactions": "number"
		},
        {
        	...
        }
    ]
}
```

- **Получение графика пользователей по количеству реакций** 
`GET /users/leaderboard` (указывать тип сортировки здесь не требуется)


###### request:
```json
{
  "type": "graph",
}
```

###### response:
```html
<img src="leaderboard.png">
```