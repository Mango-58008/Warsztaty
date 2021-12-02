from hash_tools import hash_password, check_password, generate_salt
from psycopg2 import connect, OperationalError, errors
import datetime


class User:
    def __init__(self, username="", password="", salt=""):
        self.username = username
        self._id = -1
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    # def save_to_db(self, cursor):
    #     if self._id == -1:
    #         sql = """
    #         insert into users(username, hashed_password)
    #         values(%s, %s) returning id
    #         """
    #         values = (self.username, self.hashed_password)
    #         cursor.execute(sql, values)
    #         self._id = cursor.fetchone()[0] # or [id]
    #         return True
    #     else:
    #         sql = """
    #         update users set username=%s, hashed_password=%s where id=%s
    #         """
    #         values = (self.username, self.hashed_password, self.id)
    #         cursor.execute(sql, values)
    #         return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """
        select id, username, hashed_password from users where username=%s
        """
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            result = [loaded_user.username, loaded_user._id, loaded_user._hashed_password]
            return result
            # return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = """
        select id, username, hashed_password from users where id=%s
        """
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            result = [loaded_user.username, loaded_user._id, loaded_user.hashed_password]
            return result
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = """
        select id, username, hashed_password from users
        """
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self, cursor):
        sql = """
        delete from users where id=%s
        """
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    def __init__(self, from_id, to_id, text):
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None
        self._id = -1

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """
            insert into messages(from_id, to_id, creation_date, text)
            values(%s, %s, %s, %s) returning id
            """
            values = (self.from_id, self.to_id, datetime.datetime.now(), self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        return False

    @staticmethod
    def load_all_messages(cursor):
        sql = """
        select id, from_id, to_id, creation_date, text from messages
        """
        result = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            single_message = Message(from_id, to_id, text)
            single_message._id = id_
            single_message._creation_date = creation_date
            result.append(single_message)
        return result


cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
cnx.autocommit = True
cursor = cnx.cursor()
# Piotr = User('Piotr', 'TajnyKod')
# PiOtr = User('PiOtr', 'TajnyKOd')
# Magda = User('Magda', 'Heheszki')
# PiOtr.save_to_db(cursor)
# Magda.save_to_db(cursor)
# Piotr.save_to_db(cursor)
# print(User.load_user_by_username(cursor, 'Piotr'))
# print(User.load_user_by_username(cursor, 'PiOtr'))
# print(User.load_user_by_id(cursor, '3'))
# print(User.load_all_users(cursor))
# Piotr.delete_user(cursor)


# m1 = Message(3, 7, "A kto jest małą kizią mizią?!")
# m2 = Message(7, 3, "Nie ja")
# m3 = Message(3, 7, "No Tyyyy")
# m4 = Message(7, 3, "No jaaa")
# m5 = Message(3, 7, "A nie mówiłem?!")
#
# m1.save_to_db(cursor)
# m2.save_to_db(cursor)
# m3.save_to_db(cursor)
# m4.save_to_db(cursor)
# m5.save_to_db(cursor)

# print(Message.load_all_messages(cursor))

cursor.close()
cnx.close()
