"""
All routes for user interaction
"""
from src.modules import app
from flask import request
import matplotlib.pyplot as plt
from src.modules.checker import check_email, check_username
from src.modules.email_checker import send_verification_msg
import src.database.db as db
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

            if not (db.check_email_in_db(email=email)):
                return {"error": "current email is busy. Please, enter another one"}, 400

            if db.get_user_db(username=username) is not None:
                return {"error": "current username is busy. Please, enter another one"}, 400

            if not (check_username(username=username)):
                return {"error": "incorrect username"}, 400

            send_verification_msg(email=email, username=username)

        user_uuid = str(uuid4())
        db.add_user_db(first_name, last_name, email, username, 0, False, user_uuid)
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
    user = db.get_user_db(**data)
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

        user = db.get_user_db(username=username)

        if len(user) == 0:
            return {"error": f"user with username {username} does not exist"}, 404

        status = user[5]
        if int(status) == 0:
            return {"error": f"user with username {username} does not confirmed"}, 403

        if not (db.check_post_db(username=username, title=title)):
            return {"error": "current title is already exist for the user"}, 400

        post_id = str(uuid4())
        db.add_post_db(title=title, author_username=username, text=text, post_id=post_id)

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
    try:
        data = request.json

        post = db.get_post_db(**data)
        if len(post) == 0:
            return {"error": "no post"}, 404

        title, username, text, post_id = post
        reactions = []
        for reaction in db.get_reactions_post_db(**data):
            reactions.append(reaction[0])
        return {
            "title": title,
            "author_username": username,
            "post_id": post_id,
            "text": text,
            "reactions": reactions,
        }, 200

    except KeyError:
        return {"error": "missing username or title or post_id does not specified"}, 400


@app.post("/posts/post/reaction")
def put_reaction():
    try:
        data = request.json
        if not ("reaction" in data):
            return {"error": "reaction does not specified"}, 400

        db.add_reaction_db(**data)

        return {}, 201

    except KeyError:
        return {"error": "missing username or title or post_id does not specified"}, 400


@app.get("/users/user/posts")
def get_user_posts():
    try:
        data = request.json
        if not ("sort" in data):
            return {"error": "sorting type does not specified"}

        posts = db.get_all_user_posts_db(**data)
        if len(posts) == 0:
            return {"error": "no post"}, 404

        return {"posts": posts}, 200

    except KeyError:
        return {"error": "missing username or title or post_id does not specified"}, 400


@app.get("/users/leaderboard")
def show_leaderboard():
    try:
        data = request.json
        lb_type = data["type"]
        if lb_type == "list":
            try:
                sort = data["sort"]

                all_users = db.get_usernames_db(sort=sort)
                total_reactions = db.get_total_reactions_db(sort=sort)

                leaderboard = []
                for i in range(1, len(all_users)+1):
                    leaderboard.append(f"{i} - {all_users[i - 1]}, reactions - {total_reactions[i - 1]}")

                return {"users": leaderboard}, 200

            except KeyError:
                return {"error": "sorting type does not exist"}, 400

        else:
            try:
                sort = data["sort"]
                usernames = db.get_usernames_db(sort=sort)
                total_reactions = db.get_total_reactions_db(sort=sort)

                plt.bar(usernames, total_reactions)
                plt.title("Leaderboard")
                plt.xlabel("Users")
                plt.ylabel("Total reactions")

                plt.savefig("leaderboard.png")
                return "<img src='leaderboard.png'>"

            except KeyError:
                return {"error": "sorting type does not exist"}, 400

    except KeyError:
        return {"error": "missing leaderboard type"}, 400


@app.delete("/posts/post/delete")
def delete_post():
    try:
        data = request.json
        db.delete_post_db(**data)
        return {"message": "post deleted successfully"}, 202

    except KeyError:
        return {"error": "username and title or post_id does not specified"}, 400


@app.delete("/users/user/delete")
def delete_user():
    try:
        data = request.json
        db.delete_user_db(**data)
        return {"message": "user deleted successfully"}, 202

    except KeyError:
        return {"error": "username and title or post_id does not specified"}, 400


@app.post("/users/user/verify")
def verify_user():
    try:
        data = request.json
        username = data["username"]
        if not"code" in data:
            return {"error": "verification code does not specified"}, 400

        code = data["code"]
        if db.check_verify_db(username=username, code=code) is True:
            return {"message": f"user with username {username} successfully confirmed"}, 201

        else:
            return {"error": "incorrect verification code"}, 400

    except KeyError:
        return {"error": "username does not specified"}, 400
