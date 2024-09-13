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
             

def table_list(cursor):
       cursor.execute(f"SELECT table_name \
                        FROM information_schema.tables \
                        WHERE table_type = 'BASE TABLE'\
                        AND table_schema = 'public'\
                        ORDER BY table_name;")
       query_result = cursor.fetchall()
       #print(query_result)
       return query_result


def all_table_column_list(cursor):
       cursor.execute(f"SELECT \
               t.table_name,\
               c.column_name,\
               c.is_nullable,\
               c.data_type\
             FROM\
               (SELECT * FROM information_schema.tables\
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE') t\
             LEFT JOIN\
               (SELECT * FROM information_schema.columns WHERE table_schema = 'public') c\
             ON\
               t.table_name = c.table_name\
             ORDER BY\
               t.table_name, c.ordinal_position;")

       query_result = cursor.fetchall()
       return query_result

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

def all_dump(cursor, table_name):
       cursor.execute(f"SELECT * FROM {table_name}")
       query_result = cursor.fetchall()
       #print(query_result)
       for record in query_result:
           #print(record)
           fmt = ""
           for i in range(len(record)):
               #print(record[i])
               fmt = fmt + "{:10} "
           #print("{:10} {:10} {:10}".format(record[0], record[1],record[2]))
           #print("{:10} {:10} {:10}".format(*record))
           print(fmt.format(*record))
             
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

def print_table(cursor):
       print("*** " +sys._getframe().f_code.co_name + " ***")
       tables = table_list(cursor)
       for table in tables:
           print(table[0])

def print_table_column(cursor):
       # https://atsum.in/database/postgresql-show-tables/
       print("*** " +sys._getframe().f_code.co_name + " ***")
       tables = table_list(cursor)
       for table in tables:
           table_name = table[0]
           column_lists = table_column_list(cursor,  table_name)
           print(column_lists[0][0])
           for c in column_lists:
               print(f"  {c[1]:10} {c[2]:10} {c[3]:10}")

def print_table_data(cursor):
       # https://atsum.in/database/postgresql-show-tables/
       print("*** " +sys._getframe().f_code.co_name + " ***")
       tables = table_list(cursor)
       for table in tables:
           table_name = table[0]
           all_dump(cursor, table_name)

def main():
    try:
       (host, dbname, username, password) = get_dbinfo()
       connection = get_connect(host, dbname, username, password )
       cursor = connection.cursor()

       tables = table_list(cursor)
       for table in tables:
           print(table[0])

       #all_table_column_lists = all_table_column_list(cursor)
       #column_lists = table_column_list(cursor,  "users")
       #print(column_lists[0][0])
       #for c in column_lists:
       #    print(f"  {c[1]:10} {c[2]:10} {c[3]:10}")
       #column_lists = table_column_list(cursor,  "posts")
       #print(column_lists[0][0])
       #for c in column_lists:
       #    print(f"  {c[1]:10} {c[2]:10} {c[3]:10}")

       ###
       print("")
       print_table(cursor)
       print("")
       print_table_column(cursor)

       print("")
       print_table_data(cursor)
       print("")
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


