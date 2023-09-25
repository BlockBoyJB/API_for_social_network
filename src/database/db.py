import sqlite3 as data


def add_user_db(first_name: str, last_name: str, email: str, username: str,
                total_reactions: int, status: bool, user_uuid: str):

    user = (first_name, last_name, email, username, total_reactions, status, user_uuid)

    connection = data.connect("app_db.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users values (?, ?, ?, ?, ?, ?, ?)", user)

    connection.commit()
    connection.close()


def get_user_db(username: str):
    connection = data.connect("app_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchall()
    connection.close()
    return user


def add_post_db(title: str, author_username: str, text: str, post_id: str):
    post = (title, author_username, text, post_id)
    connection = data.connect("app_db.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts values (?, ?, ?, ?)", post)

    connection.commit()
    connection.close()


def get_post_db(username: str, title: str):
    connection = data.connect("app_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE author_username=? and title=?", (username, title))
    user = cursor.fetchall()
    connection.close()
    return user


def add_reaction_db(reaction: str, username: str, title: str):
    connection = data.connect("app_db.db")
    cursor = connection.cursor()
    post_id = cursor.execute("SELECT post_id FROM posts WHERE title=? and author_username=?", (title, username))
    cursor.execute("INSERT INTO reactions values (?, ?)", (reaction, post_id))

    connection.commit()
    connection.close()


def get_reactions_post_db(username: str, title: str):
    connection = data.connect("app_db.db")
    cursor = connection.cursor()
    post_id = cursor.execute("SELECT post_id FROM posts WHERE author_username=? and title=?", (username, title))

    cursor.execute("SELECT name FROM reactions WHERE post_id=?", (post_id,))
    reactions = cursor.fetchall()
    connection.close()
    return reactions


# add_user_db('vasya', 'pupkin', 'asasf', '@vasek', 0, False, 'asgasfsfasf')
# print(get_user_db('@vasek'))
# add_post_db("new title", "@vasek", "second text", 'gassfaf123123')
print(get_post_db("@vasek", "new title"))
