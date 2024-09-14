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
       print(f"{table_name:16}  {query_result}")

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
             
def insert_text(cursor, table_name, data):
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
       line_insert(cursor, table_name, sql, column_type_list, data)

def insert(cursor, table_name, data_tuple):
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
       cursor.execute(sql, data_tuple)

#def update(cursor, table_name, column_name_list,print_fmt ,where, data):
def test_update_(cursor):
       table_name = "topping"
       column_name = "name"
       fmt = "%s"
       where = "topping_id"
       sql = f"UPDATE {table_name} set  {column_name}  = {fmt} WHERE {where} = %s"
       cursor.execute(sql, ('AAAA',5))

def test_update_multi_(cursor):
       table_name = "topping"
       column_name = "(name, size)"
       fmt = "(%s, %s)"
       where = "topping_id"
       sql = f"UPDATE {table_name} set  {column_name}  = {fmt} WHERE {where} = %s"
       cursor.execute(sql, ('おかか','L', 4))

def test_update(cursor):
       table_name = "topping"
       column_name = "name"
       fmt = "%s"
       where = "topping_id = 5"
       sql = f"UPDATE {table_name} set  {column_name}  = {fmt} WHERE {where} "
       cursor.execute(sql, ('AAAA',))

def test_update_multi(cursor):
       table_name = "topping"
       column_name = "(name, size)"
       fmt = "(%s, %s)"
       where = "topping_id = 4"
       sql = f"UPDATE {table_name} set  {column_name}  = {fmt} WHERE {where} "
       cursor.execute(sql, ('おかか','L'))

def update(cursor, table_name, where, column_name, fmt, data_tuple):
       #table_name = "topping"
       #column_name = "(name, size)"
       #fmt = "(%s, %s)"
       #where = "topping_id = 4"
       sql = f"UPDATE {table_name} set  {column_name}  = {fmt} WHERE {where} "
       cursor.execute(sql, data_tuple)

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


#* ramen
#* topping
#* type_of_noodle           
#* noodle_hardness          
#* soup_thickness           
#* amount_of_oil            
#* sex                      


# customer                 
# customer_customer_id_seq 
# order_list               
# order_list_order_id_seq  
# order_topping            

table_list = [
"ramen",
"ramen_price",
"topping",
"topping_price",
"type_of_noodle",
"noodle_hardness",
"soup_thickness",
"amount_of_oil",
"sex",
"customer"
]


def main():
    try:
       (host, dbname, username, password) = get_dbinfo()
       #connection = get_connect("localhost", "test02", "username", "password" )
       connection = get_connect(host, dbname, username, password )
       cursor = connection.cursor()

       cursor.execute(f"DELETE FROM order_topping;")
       cursor.execute(f"DELETE FROM order_list;")
       #all_delete(cursor)
       #insert(cursor)

       #delete(cursor, "ramen")
       #delete(cursor, "topping")
       #csv_load(cursor, "ramen",      "./data/ramen.csv")
       #csv_load(cursor, "topping",      "./data/topping.csv")
       #all_dump(cursor, "ramen")
       #all_dump(cursor, "topping")

       for table in reversed(table_list):
           delete(cursor, table)

       for table in table_list:
           print(table)
           csv_load(cursor, table,   f"./data/{table}.csv")
       
       #insert_text(cursor, "topping",   "5,ねぎ,S,JP")
       #insert_text(cursor, "topping_price",   "5,10")

       insert(cursor, "topping",   (5,'ねぎ','S','JP'))
       insert(cursor, "topping_price",   (5,10))

       for table in table_list:
           all_dump(cursor, table)

       #all_dump(cursor, "topping")
       #test_update(cursor)
       #all_dump(cursor, "topping")
       #test_update_multi(cursor)
       #all_dump(cursor, "topping")

       all_dump(cursor, "topping")

       table_name = "topping"
       where = "topping_id = 5"
       column_name = "name"
       fmt = "%s"
       data_tuple = ('AAAA',)
       update(cursor, table_name, where, column_name, fmt, data_tuple)

       all_dump(cursor, "topping")

       table_name = "topping"
       where = "topping_id = 4"
       column_name = "(name, size)"
       fmt = "(%s, %s)"
       data_tuple = ('おかか','L')
       update(cursor, table_name, where, column_name, fmt, data_tuple)

       all_dump(cursor, "topping")

       insert(cursor, "order_list",   (20240911001,3,1,2000,"2024-01-08 04:05:06"))
       insert(cursor, "order_topping",   (20240911001,1))
       insert(cursor, "order_topping",   (20240911001,3))
       all_dump(cursor, "order_list")
       all_dump(cursor, "order_topping")


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


