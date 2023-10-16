from src.modules import app
from flask import request
import matplotlib.pyplot as plt
from src.modules.classes import UserStorage, User, Post, PostStorage
from src.modules.checker import check_email, check_username
from src.modules.email_checker import EmailVerification

storage = UserStorage()
post_storage = PostStorage()
verification_service = EmailVerification()


# создание пользователя
@app.post("/users/create")
def initialization_user():
    try:
        data = request.json
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        username = data["username"]

        if app.debug is False:
            # проверка почты на корректность.
            if not(check_email(email=email)):
                return {"error": "incorrect email"}, 400

            if email in storage.get_all_emails():  # проверяем, что указанной почты нет среди зарегистрированных
                return {"error": "current email is busy. Please, enter another one"}, 400

            if not(check_username(username=username)):
                return {"error": "incorrect username"}, 400

            if username in storage.get_all_usernames():
                return {"error": "current username is busy. Please, enter another one"}, 400

            verification_service.send_verification_msg(email=email, username=username)

        # создаем запись о пользователе
        storage.add_email(email=email)
        storage.add_username(username=username)
        storage.add(User(first_name=first_name, last_name=last_name, email=email, username=username))

        return {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "total_reactions": 0,
            "posts": [],
            "status": "unconfirmed",
            "message": "check_your_email",
        }, 201

    except KeyError:
        return {"error": "missing data"}, 400


# получение информации о пользователе
@app.get("/users/<username>")
def get_user(username):
    user = storage.get_user(username=username)
    if user is False:
        return {"error": f"user with username {username} does not exist"}, 400

    else:
        return user.show_user(), 200


# создание поста
@app.post("/posts/create")
def create_post():
    try:
        data = request.json
        username = data["username"]
        title = data["title"]
        text = data["text"]

        user: User = storage.get_user(username)

        if user is False:
            return {"error": f"user with username {username} does not exist"}, 404

        if user.get_status() is False:
            return {"error": f"user with username {username} does not confirmed"}, 403

        user.add_title_post(title=title)
        new_post = Post(title=title, author_username=username, text=text)
        post_storage.add(entry=new_post)
        user.add_post(post=new_post)
        return {
            "title": title,
            "username": username,
            "text": text,
            "reactions": [],
            "ID": new_post.get_id(),
        }, 201

    except KeyError:
        return {"error": "missing data"}, 400


# получение информации о посте
@app.get("/posts/post")
def get_post():
    data = request.json

    if "post_id" in data:  # получение поста через уникальный id
        post_id = data["post_id"]
        post = post_storage.get_post(post_id=post_id)
        if post is False:
            return {"error": f"post with id {post_id} does not exist"}, 404

        else:
            return post.show_post(), 200

    else:  # либо через имя пользователя и название
        try:
            username = data["username"]
            title = data["title"]

            user = storage.get_user(username=username)
            if user is not False:
                post = user.get_post(title=title)
                if post is False:
                    return {"error": f"post with title {title} does not exist"}, 404
                return post.show_post(), 200

            else:
                post = post_storage.get_post_with_usename(username=username)
                if post is False:
                    return {"error": f"post with title {title} does not exist"}, 404
                return post.show_post()

        except KeyError:
            return {"error": "missing data"}, 400


# создание реакции к посту
@app.post("/posts/post/reaction")
def put_reaction():
    try:
        data = request.json
        reaction = data["reaction"]

        if "post_id" in data:
            post_id = data["post_id"]

            post = post_storage.get_post(post_id)
            post.set_reaction(reaction=reaction)

            user = storage.get_user(post.get_author_username())
            user.add_reaction()
            return {}, 201

        else:
            try:
                username = data["username"]
                title = data["title"]

                user = storage.get_user(username=username)
                user.add_reaction()

                post = user.get_post(title=title)
                post.set_reaction(reaction=reaction)
                return {}, 201

            except KeyError:
                return {"error": "username or post title is not specified"}, 400

    except KeyError:
        return {"error": "reaction does not specified"}, 400


# получение информации о всех постах пользователя
@app.get("/users/<username>/posts")
def get_user_posts(username):
    try:
        data = request.json
        sort = data["sort"]

        # проверяем, что пользователь существует
        if storage.get_user(username=username) is False:
            return {"error": f"user with id {username} does not exist"}, 404

        user_posts = post_storage.get_all_users_posts(username=username)
        if user_posts is False:
            return {"error": "no posts"}, 404

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

            usersnames = [user.get_username() for user in storage.get_all_users()]
            users_total_reactions = [user.get_reactions() for user in storage.get_all_users()]

            plt.bar(usersnames, users_total_reactions)
            plt.title("Leaderboard")
            plt.xlabel("Users")
            plt.ylabel("Total reactions")

            plt.savefig("leaderboard.png")
            return '<img src="leaderboard.png">'

    except KeyError:
        return {"error": "missing leaderboard type"}, 400


@app.delete("/posts/post/delete")
def delete_post():
    data = request.json
    if "post_id" in data:
        post_id = data["post_id"]

        post = post_storage.get_post(post_id=post_id)
        if post is False:
            return {"error": f"post with id {post_id} does not exist"}, 404
        title = post.get_title()
        username = post.get_author_username()
        user = storage.get_user(username=username)
        if user.remove_post(title=title) is True and post_storage.delete_post(title=title) is True:
            return {"message": "post deleted successfully"}, 202

        else:
            return {"error": "something is wrong"}

    else:
        try:

            username = data["username"]
            title = data["title"]

            user: User = storage.get_user(username)

            if user.remove_post(title=title) is True and post_storage.delete_post(title=title) is True:
                return {"message": "post deleted successfully"}, 202

            else:
                return {"error": "post or user does not exist"}, 404

        except KeyError:
            return {"error": "username or title does not specified"}, 400


@app.delete("/users/<username>/delete")
def delete_user(username):
    if storage.delete_user(username=username) is True:
        return {"message": f"user with username {username} deleted successfully"}, 202
    return {"error": f"user with username {username} does not exist"}, 404


@app.post("/users/<username>/verify")
def verify_user(username):
    codes = verification_service.get_codes()
    try:
        data = request.json
        if not"code" in data:
            return {"error": "verification code does not specified"}, 400

        code = data["code"]
        user_code = codes[username]
        if user_code == code:
            user = storage.get_user(username=username)
            user.verify_user()
            return {"message": f"user with username {username} successfully confirmed"}, 201

        else:
            return {"error": "incorrect verification code"}, 400

    except KeyError:
        return {"error": f"user with username {username} does not exist"}, 404


if __name__ == '__main__':
    app.run()
