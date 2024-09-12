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
       cursor.execute("DELETE FROM posts;")
       cursor.execute("DELETE FROM users;")

def insert(cursor):
       sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
       cursor.execute(sql, (1,"西草", "devg1120@gmail.com"))
       cursor.execute(sql, (2,"山田", "yamada@gmail.com"))

def line_insert(cursor,table_name, line):
       line2 = line.strip()
       print(line2)
       if table_name == "users":
          param = line2.split(',')
          p1 = int(param[0].strip())
          p2 = param[1].strip()
          p3 = param[2].strip()
          #print(f"_{p1}_")
          #print(f"_{p2}_")
          #print(f"_{p3}_")
          sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
          cursor.execute(sql, (p1,p2,p3))

       elif table_name == "posts":
          param = line2.split(',')
          p1 = int(param[0].strip())
          p2 = param[1].strip()
          p3 = param[2].strip()
          p4 = param[3].strip()
          #print(f"_{p1}_")
          #print(f"_{p2}_")
          #print(f"_{p3}_")
          #print(f"_{p4}_")
          sql = "INSERT INTO posts (id, user_id, title, body) VALUES (%s, %s, %s, %s)"
          cursor.execute(sql, (p1,p2,p3,p4))

def csv_load(cursor, table_name, csv_filepath):
       with open(csv_filepath) as f:
          for line in f:
             line2 =  line.rstrip()
             if line2 == "":
                 continue
             if line2.startswith('#'):
                 continue
             m = re.match('(.+ )\#(.+)$',line2)
             if m == None:
                 line_insert(cursor, table_name, line2)
             else:
                 line_insert(cursor, table_name, m.group(1))
             


def all_dump(cursor, table_name):
       cursor.execute(f"SELECT * FROM {table_name}")
       query_result = cursor.fetchall()
       print(query_result)

def main():
    try:
       connection = get_connect("localhost", "test01", "username", "password" )
       cursor = connection.cursor()

       all_delete(cursor)
       #insert(cursor)
       csv_load(cursor, "users", "./users.csv")
       csv_load(cursor, "posts", "./posts.csv")
       all_dump(cursor, "users")
       all_dump(cursor, "posts")
       
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


