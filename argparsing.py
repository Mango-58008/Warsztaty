import argparse
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from hash_tools import check_password, hash_password
from models import User



parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


def create_user(cursor, username, password):
    if len(password) < 8:
        print("Too short password.")
    else:
        try:
            user = User(username, password)
            user.save_to_db(cursor)
            print("Added user")
        except UniqueViolation as e:
            print("Username already taken. ", e)


def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User doesnt exist.")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password too short.")
        else:
            user[2] = hash_password(new_pass)
            user.save_to_db(cursor)
            print("Password changed")


if __name__ == "__main__":
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        else:
            print("Something went wrong.")
    except OperationalError as e:
        print("Error occurred: ", e)

    cursor.close()
    cnx.close()
