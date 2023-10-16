"""
The logic of interaction with the database
"""
import sqlite3 as data


DB_ADRESS = "src/database/app_db.db"


def add_user_db(first_name: str, last_name: str, email: str, username: str,
                total_reactions: int, status: bool, user_uuid: str):

    user = (first_name, last_name, email, username, total_reactions, status, user_uuid)

    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users values (?, ?, ?, ?, ?, ?, ?)", user)

    connection.commit()
    connection.close()


def get_user_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if "user_id" in kwargs:
        cursor.execute("SELECT * FROM users WHERE user_uuid=?", (kwargs["user_id"],))

    else:
        cursor.execute("SELECT * FROM users WHERE username=?", (kwargs["username"],))

    user = cursor.fetchone()
    connection.close()
    return user


def delete_user_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if "user_id" in kwargs:
        cursor.execute("DELETE FROM users WHERE user_uuid=?", (kwargs["user_id"],))

    else:
        cursor.execute("DELETE FROM users WHERE username=?", (kwargs["username"],))

    connection.commit()
    connection.close()


def get_usernames_db(sort):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if sort == "desc":
        cursor.execute("SELECT username FROM users ORDER BY total_reactions DESC")
    else:
        cursor.execute("SELECT username FROM users ORDER BY total_reactions")

    users = []
    for user in cursor.fetchall():
        users.append(user[0])

    connection.close()

    return users


def get_total_reactions_db(sort):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if sort == "desc":
        cursor.execute("SELECT total_reactions FROM users ORDER BY total_reactions DESC")
    else:
        cursor.execute("SELECT total_reactions FROM users ORDER BY total_reactions")

    reactions = []
    for reaction in cursor.fetchall():
        reactions.append(reaction[0])

    connection.close()

    return reactions


def check_email_in_db(email: str):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT email FROM users WHERE email=?)", (email, ))

    status = cursor.fetchone()[0]
    connection.close()
    if status == 1:
        return False
    return True


def add_post_db(title: str, author_username: str, text: str, post_id: str):
    post = (title, author_username, text, post_id)
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts values (?, ?, ?, ?)", post)

    connection.commit()
    connection.close()


def get_post_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if "post_id" in kwargs:
        cursor.execute("SELECT * FROM posts WHERE post_id=?", (kwargs["post_id"],))

    else:
        title = kwargs["title"]
        username = kwargs["username"]
        cursor.execute("SELECT * FROM posts WHERE author_username=? and title=?", (username, title,))

    post = cursor.fetchone()
    connection.close()
    return post


def delete_post_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if "post_id" in kwargs:
        cursor.execute("DELETE FROM posts WHERE post_id=?", (kwargs["post_id"],))

    else:
        title = kwargs["title"]
        username = kwargs["username"]
        cursor.execute("DELETE FROM posts WHERE title=? and author_username=?", (title, username,))

    connection.commit()
    connection.close()


def check_post_db(username: str, title: str):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT title FROM posts WHERE author_username=? and title=?)", (username, title,))

    status = cursor.fetchone()[0]
    connection.close()
    if status == 1:
        return False
    return True


def add_reaction_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    reaction = kwargs["reaction"]
    if "post_id" in kwargs:
        cursor.execute("INSERT INTO reactions values (?, ?)", (reaction, kwargs["post_id"],))

    else:
        username = kwargs["username"]
        title = kwargs["title"]
        cursor.execute("SELECT post_id FROM posts WHERE author_username=? and title=?", (username, title,))
        post_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO reactions values (?, ?)", (reaction, post_id,))

        cursor.execute("SELECT total_reactions FROM users WHERE username=?", (username,))
        total_reactions = cursor.fetchone()[0]
        cursor.execute("UPDATE users SET total_reactions=? WHERE username=?", (total_reactions + 1, username,))

    connection.commit()
    connection.close()


def get_reactions_post_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if "post_id" in kwargs:
        cursor.execute("SELECT name FROM reactions WHERE post_id=?", (kwargs["post_id"],))

    else:
        username = kwargs["username"]
        title = kwargs["title"]
        cursor.execute("SELECT post_id FROM posts WHERE author_username=? and title=?", (username, title,))
        post_id = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM reactions WHERE post_id=?", (post_id, ))

    reactions = cursor.fetchall()
    connection.close()
    return reactions


# I warn you, the following is the shit code. I don't want to think about the logic of normal sorting (=
def get_all_user_posts_db(**kwargs):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    if "user_id" in kwargs:
        cursor.execute("SELECT username FROM users WHERE user_uuid=?", (kwargs["user_id"], ))
        username = cursor.fetchone()[0]

    else:
        username = kwargs["username"]

    sort = kwargs["sort"]
    condition = True if (sort == "desc") else False
    cursor.execute("SELECT * FROM posts WHERE author_username=?", (username,))
    posts = cursor.fetchall()
    all_post = []
    for post in posts:
        title, author_username, text, post_id = post
        cursor.execute("SELECT name FROM reactions WHERE post_id=?", (post_id, ))
        reactions = cursor.fetchall()
        all_post.append((len(reactions), title, author_username, text, post_id))

    all_post.sort(reverse=condition)

    response = []

    for post in all_post:
        r, title, author_username, text, post_id = post
        cursor.execute("SELECT name FROM reactions WHERE post_id=?", (post_id,))
        post_reactions = []
        reactions = cursor.fetchall()
        for reaction in reactions:
            post_reactions.append(reaction[0])
        response.append({
            "username": author_username,
            "title": title,
            "post_id": post_id,
            "text": text,
            "reactions": post_reactions
        })

    connection.close()

    return response


def add_verification_db(username: str, code: str):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO verification_codes VALUES (?, ?)", (username, code,))

    connection.commit()
    connection.close()


def check_verify_db(username: str, code: str):
    connection = data.connect(DB_ADRESS)
    cursor = connection.cursor()
    cursor.execute("SELECT code FROM verification_codes WHERE username=?", (username,))
    correct_code = cursor.fetchone()[0]
    if code == correct_code:
        cursor.execute("UPDATE users SET status=? WHERE username=?", (1, username,))
        cursor.execute("DELETE FROM verification_codes WHERE username=?", (username,))
        connection.commit()
        connection.close()
        return True

    else:
        connection.close()
        return False
