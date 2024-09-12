import sys
import traceback
import re

import psycopg2
from psycopg2.extensions import connection


#print(psycopg2.apilevel)


def get_connect( hostname, dbname,username, password) -> connection:
    target = f"host={hostname} dbname={dbname} user={username} password={password}"
    return psycopg2.connect(target)


def all_delete(cursor):
       cursor.execute("DELETE FROM users;")

def insert(cursor):
       sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
       cursor.execute(sql, (1,"西草", "devg1120@gmail.com"))
       cursor.execute(sql, (2,"山田", "yamada@gmail.com"))

def all_dump(cursor):
       cursor.execute("SELECT * FROM users")
       query_result = cursor.fetchall()
       print(query_result)

def main():
    try:
       connection = get_connect("localhost", "test01", "username", "password" )
       cursor = connection.cursor()

       #all_delete(cursor)
       #insert(cursor)
       all_dump(cursor)
       
       cursor.close()
       connection.commit()

    #except Exception  as e:
    #   #print(dir(e))
    #   #print("Exception class:", e.__class__.__name__)
    #   #print("Exception args.len:", len(e.args))
    #   #print("Exception args:", e.args[0])
    #   #print("Exception args:", e)
    #   print(f"{e.__class__.__name__}: {e}") 
    except Exception as e:
        error_class = type(e)
        error_description = str(e)
        err_msg = '%s: %s' % (error_class, error_description)
        print(err_msg)
        tb = traceback.extract_tb(sys.exc_info()[2])
        trace = traceback.format_list(tb)
        print('---- traceback ----')
        for line in trace:
            if '~^~' in line:
                print(line.rstrip())
            else:
                text = re.sub(r'\n\s*', ' ', line.rstrip())
                print(text)
        print('-------------------')
    
    
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()


