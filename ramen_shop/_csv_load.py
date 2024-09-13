import sys
import traceback
import re

import psycopg2
from psycopg2.extensions import connection

# "./_dbname_" ファイルの導入
#

#print(psycopg2.apilevel)


def get_connect( hostname, dbname,username, password) -> connection:
    target = f"host={hostname} dbname={dbname} user={username} password={password}"
    return psycopg2.connect(target)


def all_delete(cursor):
       cursor.execute("DELETE FROM posts;")
       cursor.execute("DELETE FROM users;")

def delete(cursor, table):
       cursor.execute(f"DELETE FROM {table};")

def insert(cursor):
       sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
       cursor.execute(sql, (1,"西草", "devg1120@gmail.com"))
       cursor.execute(sql, (2,"山田", "yamada@gmail.com"))

def line_insert_self(cursor,table_name, line):
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
       elif table_name == "user_cards":
          param = line2.split(',')
          p1 = int(param[0].strip())
          p2 = param[1].strip()
          p3 = param[2].strip()
          #print(f"_{p1}_")
          #print(f"_{p2}_")
          #print(f"_{p3}_")
          sql = "INSERT INTO user_cards (id, user_id, card_number) VALUES (%s, %s, %s)"
          cursor.execute(sql, (p1,p2,p3))

def table_column_list(cursor, table_name):
       TABLE = table_name
       cursor.execute(f"SELECT \
               t.table_name,\
               c.column_name,\
               c.is_nullable,\
               c.data_type\
             FROM\
               (SELECT * FROM information_schema.tables\
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name = '{TABLE}') t\
             LEFT JOIN\
               (SELECT * FROM information_schema.columns WHERE table_schema = 'public') c\
             ON\
               t.table_name = c.table_name\
             ORDER BY\
               t.table_name, c.ordinal_position;")

       query_result = cursor.fetchall()
       return query_result

def line_insert(cursor,table_name, sql, column_type_list, line):
       line2 = line.strip()
       print(line2)
       param = line2.split(',')
       #p1 = int(param[0].strip())
       #p2 = param[1].strip()

       #cursor.execute(sql, (p1,p2))
       p_tuple = ()
       no = 0
       for entry in column_type_list:
           print(entry[3])
           if entry[3] == 'integer':
               i =  int(param[no].strip())
               p_tuple = p_tuple + (i,)
           else:
               p = param[no].strip()
               p_tuple = p_tuple + (p,)
           no = no + 1

       cursor.execute(sql, p_tuple)



def all_dump(cursor, table_name):
       cursor.execute(f"SELECT * FROM {table_name}")
       query_result = cursor.fetchall()
       print(query_result)

def csv_load(cursor, table_name, csv_filepath):
       print("***csv_load")
       column_type_list = table_column_list(cursor, table_name)
       column_name_list = ""
       print_fmt = ""
       for entry  in column_type_list:
           print(entry [1])
           column_name_list +=  entry [1] + ","
           print_fmt += "%s,"

       column_name_list = column_name_list.rstrip(",")
       print_fmt = print_fmt.rstrip(",")

       #   sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
       sql = f"INSERT INTO {table_name} ( {column_name_list} ) VALUES ({print_fmt})"
       print(sql)
       with open(csv_filepath) as f:
          for line in f:
             line2 =  line.rstrip()
             if line2 == "":
                 continue
             if line2.startswith('#'):
                 continue
             m = re.match('(.+ )\#(.+)$',line2)
             if m == None:
                 line_insert(cursor, table_name, sql, column_type_list, line2)
             else:
                 line_insert(cursor, table_name, sql, column_type_list, m.group(1))
             
def get_dbinfo():
       host = "localhost"
       dbname = ""
       username = "username"
       password = "password"

       with open("./_env_") as f:
          for line in f:
             line2 =  line.rstrip()
             if line2 == "":
                 continue
             if line2.startswith('#'):
                 continue
             m = re.match('(.+ )\#(.+)$',line2)
             line3 = ""
             if m == None:
                 line3 = line2
             else:
                 line3 = m.group(1)

             param = line3.split(':')
             if param[0] == "dbname":
                 print("set dbname:", param[1])
                 dbname = param[1]
       return (host, dbname, username, password )

def main():
    try:
       (host, dbname, username, password) = get_dbinfo()
       #connection = get_connect("localhost", "test02", "username", "password" )
       connection = get_connect(host, dbname, username, password )
       cursor = connection.cursor()

       #all_delete(cursor)
       delete(cursor, "ramen")
       #insert(cursor)
       csv_load(cursor, "ramen",      "./data/ramen.csv")
       all_dump(cursor, "ramen")
       
       cursor.close()
       connection.commit()

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


