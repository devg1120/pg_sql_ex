
import psycopg2

print(psycopg2.apilevel)

#connection = psycopg2.connect("host=localhost dbname=postgres user=<your db username> password=<your db password>")
connection = psycopg2.connect("host=localhost dbname=test01 user=username password=password")
cursor = connection.cursor()

sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
cursor.execute(sql, (1,"西草", "devg1120@gmail.com"))
cursor.execute(sql, (2,"山田", "yamada@gmail.com"))


cursor.execute("SELECT * FROM users")
query_result = cursor.fetchall()
print(query_result)

