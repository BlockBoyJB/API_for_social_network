import sqlite3 as data


def add_user_db(first_name: str, last_name: str, email: str, username: str,
                total_reactions: int, status: bool, user_uuid: str):

    user = (first_name, last_name, email, username, total_reactions, status, user_uuid)

    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users values (?, ?, ?, ?, ?, ?, ?)", user)

    connection.commit()
    connection.close()


def get_user_db(**kwargs):
    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    if "user_id" in kwargs:
        cursor.execute("SELECT * FROM users WHERE user_uuid=?", (kwargs["user_id"],))

    else:
        cursor.execute("SELECT * FROM users WHERE username=?", (kwargs["username"],))

    user = cursor.fetchone()
    connection.close()
    return user


def check_email_in_db(email: str):
    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT email FROM users WHERE email=?)", (email, ))
    if str(cursor.fetchone())[1:2] == '1':
        return True
    return False


def add_post_db(title: str, author_username: str, text: str, post_id: str):
    post = (title, author_username, text, post_id)
    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts values (?, ?, ?, ?)", post)

    connection.commit()
    connection.close()


def get_post_db(**kwargs):
    connection = data.connect("src/database/app_db.db")
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


def add_reaction_db(**kwargs):
    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    reaction = kwargs["reaction"]
    if "post_id" in kwargs:
        cursor.execute("INSERT INTO reactions values (?, ?)", (reaction, kwargs["post_id"],))

    else:
        username = kwargs["username"]
        title = kwargs["title"]
        cursor.execute("SELECT post_id FROM posts WHERE author_username=? and title=?", (username, title,))
        post_id = str(cursor.fetchone())[2:-3]
        cursor.execute("INSERT INTO reactions values (?, ?)", (reaction, post_id,))

    connection.commit()
    connection.close()


def get_reactions_post_db(**kwargs):
    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    if "post_id" in kwargs:
        cursor.execute("SELECT name FROM reactions WHERE post_id=?", (kwargs["post_id"],))

    else:
        username = kwargs["username"]
        title = kwargs["title"]
        cursor.execute("SELECT post_id FROM posts WHERE author_username=? and title=?", (username, title,))
        post_id = str(cursor.fetchone())[2:-3]
        cursor.execute("SELECT name FROM reactions WHERE post_id=?", (post_id, ))

    reactions = cursor.fetchall()
    connection.close()
    return reactions


# предупреждаю, дальше изложен гавнокод. Думать над логикой нормальной сортировки мне не хочеца
def get_all_user_posts_db(**kwargs):
    connection = data.connect("src/database/app_db.db")
    cursor = connection.cursor()
    if "user_id" in kwargs:
        cursor.execute("SELECT username FROM users WHERE user_uuid=?", (kwargs["user_id"], ))
        username = str(cursor.fetchone())[2:-3]

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
            post_reactions.append(str(reaction)[2:-3])
        response.append({
            "username": author_username,
            "title": title,
            "post_id": post_id,
            "text": text,
            "reactions": post_reactions
        })

    return response
