from psycopg2 import OperationalError, connect, errors
from models import User


USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"


def execute_create_sql(sql):
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = []
            for row in cursor:
                result.append(row)
            return result
    except OperationalError as e:
        return f"Wystąpił błąd: {e}"
    except errors.DuplicateDatabase:
        print("Baza o tej nazwie już istnieje.")
    else:
        cursor.close()
        cnx.close()


def execute_sql(sql, db):
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = []
            for row in cursor:
                result.append(row)
            return result
    except OperationalError as e:
        return f"Wystąpił błąd: {e}"
    except errors.DuplicateTable:
        print(f"Tabela o nazwie |{sql[sql.lower().find('table') + 6:sql.find('(')]}| już istnieje.")
    else:
        cursor.close()
        cnx.close()


create_db_sql = "create database workshop"
execute_create_sql(create_db_sql)

cr_tb_users_sql = """
create table users(
id serial, 
username varchar(255) not null, 
hashed_password varchar(80) not null, 
primary key(id)
);
"""
execute_sql(cr_tb_users_sql, 'workshop')

cr_tb_messages_sql = """
create table messages(
id serial, 
from_id int not null, 
to_id int not null, 
creation_date timestamp default current_timestamp, 
text varchar(255), 
primary key(id), 
foreign key(from_id) references users(id), 
foreign key(to_id) references users(id)
);
"""
execute_sql(cr_tb_messages_sql, 'workshop')

piotr = User('Piotr', 'TajnyKod')

