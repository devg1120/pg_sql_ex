import sys
import psycopg2
from psycopg2.extensions import connection


#print(psycopg2.apilevel)


def get_connect( hostname, dbname,username, password) -> connection:
    target = f"host={hostname} dbname={dbname} user={username} password={password}"
    return psycopg2.connect(target)

def main():
    connection = get_connect("localhost", "test01", "username", "password" )
    cursor = connection.cursor()
    try:
       sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
       cursor.execute(sql, (1,"西草", "devg1120@gmail.com"))
       cursor.execute(sql, (2,"山田", "yamada@gmail.com"))
       
       
       cursor.execute("SELECT * FROM users")
       query_result = cursor.fetchall()
       print(query_result)
       cursor.close()
       connection.commit()

    except Exception  as e:
       #print(dir(e))
       #print("Exception class:", e.__class__.__name__)
       #print("Exception args.len:", len(e.args))
       #print("Exception args:", e.args[0])
       #print("Exception args:", e)
       print(f"{e.__class__.__name__}: {e}") 


    connection.close()


if __name__ == "__main__":
    main()

#connection = psycopg2.connect("host=localhost dbname=test01 user=username password=password")
#cursor = connection.cursor()
#
#sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
#cursor.execute(sql, (1,"西草", "devg1120@gmail.com"))
#cursor.execute(sql, (2,"山田", "yamada@gmail.com"))
#
#
#cursor.execute("SELECT * FROM users")
#query_result = cursor.fetchall()
#print(query_result)

