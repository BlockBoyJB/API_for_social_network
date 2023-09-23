from flask import Flask, request
import matplotlib.pyplot as plt
from classes import UserStorage, User, Post, PostStorage
from email_checker import check_email
import uuid

app = Flask(__name__)

storage = UserStorage()
post_storage = PostStorage()


# создание пользователя
@app.post("/users/create")
def initialization_user():
    try:
        data = request.json
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]

        # проверка почты на корректность.
        # Следующим шагом будет отправка письма с кодом подтверждения почты, а также новый маршрут для верификации.
        # Также введу такие понятия как подтвержденная/неподтвержденная почта.
        # Пользователи без подтвержденной почты не будут иметь возможности создавать посты
        if not(check_email(email=email)):
            return {"error": "incorrect email"}, 400

        if email in storage.get_all_emails():  # проверяем, что указанной почты нет среди зарегистрированных
            return {"error": "current email is busy. Please, enter another one"}, 400

        storage.add_email(email=email)
        id_number = str(uuid.uuid4())
        storage.add(User(first_name=first_name, last_name=last_name, email=email, id_number=id_number))
        return {
            "id": id_number,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "total_reactions": 0,
            "posts": [],
        }, 201

    except KeyError:
        return {"error": "missing data"}, 400


# получение информации о пользователе
@app.get("/users/<user_id>")
def get_user(user_id):
    user = storage.get_user(user_id=user_id)
    if user is False:
        return {"error": f"user with id {user_id} does not exist"}, 400

    else:
        return user.show_user(), 200


# создание поста
@app.post("/posts/create")
def create_post():
    try:
        data = request.json
        author_id = data["author_id"]
        text = data["text"]
        post_id = str(uuid.uuid4())

        user = storage.get_user(author_id)
        user.add_post(post_id)

        new_post = Post(id_number=post_id, author_id=author_id, text=text)
        post_storage.add(new_post)
        return {
            "post_id": post_id,
            "author_id": author_id,
            "text": text,
            "reactions": [],
        }, 201

    except KeyError:
        return {"error": "missing data"}, 400


# получение информации о посте
@app.get("/posts/<post_id>")
def get_post(post_id):
    post = post_storage.get_post(post_id)
    if post is False:
        return {"error": f"post with id {post_id} does not exist"}, 400

    else:
        return post.show_post(), 200


# создание реакции к посту
@app.post("/posts/<post_id>/reaction")
def put_reaction(post_id):
    try:
        data = request.json
        reaction = data["reaction"]

        post = post_storage.get_post(post_id)
        post.set_reaction(reaction=reaction)

        user = storage.get_user(post.get_author_id())
        user.add_reaction()
        return {}, 200

    except KeyError:
        return {"error": "reaction does not specified"}, 400


# получение информации о всех постах пользователя
@app.get("/users/<user_id>/posts")
def get_user_posts(user_id):
    try:
        data = request.json
        sort = data["sort"]

        # проверяем, что пользователь существует
        if storage.get_user(user_id=user_id) is False:
            return {"error": f"user with id {user_id} does not exist"}, 400

        user_posts = post_storage.get_all_users_posts(user_id=user_id)
        if user_posts is False:
            return {"error": "no posts"}, 400

        else:
            condition = True if (sort == "desc") else False
            user_posts.sort(reverse=condition)

            response = []
            for post in user_posts:
                response.append(post.show_post())
            return {"posts": response}, 200

    except KeyError:
        return {"error": "missing data"}, 400


# лидерборд пользователей
@app.get("/users/leaderboard")
def show_leaderboard():
    try:
        data = request.json
        leaderboard_type = data["type"]
        if leaderboard_type == "list":
            try:
                sort = data["sort"]

                all_users = storage.get_all_users()
                condition = True if (sort == "desc") else False
                all_users.sort(reverse=condition)

                response = []
                for user in all_users:
                    response.append(user.show_user())

                return {"users": response}, 200

            except KeyError:
                return {"error": "sort key does not specified"}, 400

        else:

            users_first_names = [user.get_first_name() for user in storage.get_all_users()]
            users_total_reactions = [user.get_reactions() for user in storage.get_all_users()]

            plt.bar(users_first_names, users_total_reactions)
            plt.title("Leaderboard")
            plt.xlabel("Users")
            plt.ylabel("Total reactions")

            plt.savefig("leaderboard.png")
            return '<img src="leaderboard.png">'

    except KeyError:
        return {"error": "missing leaderboard type"}, 400


if __name__ == '__main__':
    app.run()
