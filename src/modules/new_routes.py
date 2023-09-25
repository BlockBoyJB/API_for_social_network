from src.modules import app
from flask import request
import matplotlib.pyplot as plt
from src.modules.checker import check_email, check_username
from src.database.db import check_email_in_db, add_user_db, get_user_db, add_post_db, get_post_db
from uuid import uuid4


@app.post("/users/create")
def initialization_user():
    try:
        data = request.json
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        username = data["username"]

        if app.debug is False:

            if not (check_email(email=email)):
                return {"error": "incorrect email"}, 400

            if not (check_email_in_db(email=email)):
                return {"error": "current email is busy. Please, enter another one"}, 400

            if len(get_user_db(username=username)) != 0:
                return {"error": "current username is busy. Please, enter another one"}, 400

            if not (check_username(username=username)):
                return {"error": "incorrect username"}, 400

            # TODO добавить отправку письма с верификацией + реализовать вместе с бд

        user_uuid = str(uuid4())
        add_user_db(first_name, last_name, email, username, 0, True, user_uuid)
        return {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "total_reactions": 0,
            "posts": [],
            "user_id": user_uuid,
            "status": "unconfirmed",
            "message": "check_your_email",
        }, 201

    except KeyError:
        return {"error": "missing data"}, 400


@app.get("/users/user")
def get_user():
    data = request.json
    user = get_user_db(**data)
    if len(user) == 0:
        return {"error": f"user with specified username does not exist"}, 400

    first_name, last_name, email, username, total_reations, status, user_uuid = user
    return {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "total_reactions": total_reations,
        "status": status,
        "uuid": user_uuid,
    }, 200


@app.post("/posts/create")
def create_post():
    try:
        data = request.json
        username = data["username"]
        title = data["title"]
        text = data["text"]

        user = get_user_db(username=username)

        if len(user) == 0:
            return {"error": f"user with username {username} does not exist"}, 404

        status = user[5]
        if int(status) == 0:
            return {"error": f"user with username {username} does not confirmed"}, 403

        post_id = str(uuid4())
        add_post_db(title=title, author_username=username, text=text, post_id=post_id)

        return {
            "title": title,
            "username": username,
            "reactions": [],
            "post_id": post_id,
        }, 201

    except KeyError:
        return {"error": "missing data"}, 400


@app.get("/posts/post")
def get_post():
    data = request.json

    post = get_post_db(**data)
    if len(post) == 0:
        return {"error": "no post"}, 404

    title, username, text, post_id = post
    return {
        "title": title,
        "author_username": username,
        "post_id": post_id,
        "text": text,
    }, 200
