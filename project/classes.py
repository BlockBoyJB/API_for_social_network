import uuid


class User:
    def __init__(self, first_name: str, last_name: str, email: str, username: str):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email

        self.__username = username
        self.__total_reactions: int = 0
        self.__posts: list = []

        self.__id = uuid.uuid4()

    def show_user(self):
        return {"username": self.__username,
                "first_name": self.__first_name,
                "last_name": self.__last_name,
                "email": self.__email,
                "total_reactions": self.__total_reactions,
                "posts": self.__posts,
                }

    def add_post(self, post):
        self.__posts.append(post)

    def add_reaction(self):
        self.__total_reactions += 1

    def get_reactions(self):
        return self.__total_reactions

    def get_first_name(self):
        return self.__first_name

    def get_username(self):
        return self.__username

    def remove_post(self, post_id) -> bool:
        for post in self.__posts:
            if post == int(post_id):
                self.__posts.remove(post)
                return True
        return False

    # переопределил методы для удобной сортировки
    def __lt__(self, other):
        # сначала сравниваем по количеству реакций на постах
        if self.__total_reactions < other.__total_reactions:
            return True
        if self.__total_reactions > other.__total_reactions:
            return False
        # потом по общему количеству постов
        if len(self.__posts) < len(other.__posts):
            return True
        return False

    def __eq__(self, other):
        return self.__total_reactions == other.__total_reactions and len(self.__posts) == len(other.__posts)

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return not (self < other) and self != other

    def __ge__(self, other):
        return not (self < other)


class Post:
    def __init__(self, id_number, author_username: str, text: str):
        self.__postname = id_number
        self.__author_username = author_username
        self.__text = text
        self.__reactions: list[str] = []

    def add_reaction(self, reaction):
        self.__reactions.append(reaction)

    def show_post(self):
        return {
            "id": self.__postname,
            "author_username": self.__author_username,
            "text": self.__text,
            "reactions": self.__reactions
        }

    def get_author_username(self):
        return self.__author_username

    def get_id(self):
        return self.__postname

    def get_reactions(self):
        return self.__reactions

    def set_reaction(self, reaction):
        self.__reactions.append(reaction)

    # переопределил методы для удобной сортировки по количеству реакций на посте
    def __lt__(self, other):
        if len(self.__reactions) < len(other.__reactions):
            return True
        return False

    def __eq__(self, other):
        return len(self.__reactions) == len(other.__reactions)

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        return not (self > other)

    def __gt__(self, other):
        return not (self < other) and self != other

    def __ge__(self, other):
        return not (self < other)


# решил разграничить 2 класса для хранения постов и пользователей
class UserStorage:
    def __init__(self):
        self.__storage: list = []

        # заведем отдельные массивы для почты и юзернейма для удобной проверки при создании пользователя
        self.__email_storage: list[str] = []
        self.__username_storage: list[str] = []

    # работа с пользователем
    def add(self, entry):
        self.__storage.append(entry)

    def get_all_usernames(self):
        return self.__username_storage

    def get_user(self, username):
        for user in self.__storage:
            if user.get_username() == username:
                return user
        return False

    def get_all_users(self):
        return self.__storage

    # работа с почтой
    def add_email(self, email):
        self.__email_storage.append(email)

    def get_all_emails(self):
        return self.__email_storage

    # работа с именами пользователей
    def add_username(self, username: str):
        self.__username_storage.append(username)

    def __len__(self):
        return len(self.__storage)


class PostStorage:
    def __init__(self):
        self.__storage = []

    def add(self, entry):
        self.__storage.append(entry)

    def get_post(self, post_id):
        for post in self.__storage:
            if post.get_id() == int(post_id):
                return post
        return False

    def delete_post(self, post_id):
        for post in self.__storage:
            if post.get_id() == int(post_id):
                self.__storage.remove(post)
                return True
        return False

    def get_all_users_posts(self, username):
        user_posts = []

        for post in self.__storage:
            if post.get_author_username() == username:
                user_posts.append(post)

        if len(user_posts) != 0:
            return user_posts
        return False

    def __len__(self):
        return len(self.__storage)
