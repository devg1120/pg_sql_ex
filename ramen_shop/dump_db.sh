DBNAME=`./get_dbname.sh`
echo ${DBNAME}



#docker exec sql_ex_postgres_1 /bin/sh -c  "pg_dump -s -h localhost -p 5432  -U username test01 > /var/dump/test01.dmp"
#cp ../dump/test01.dmp .

docker exec pg_sql_ex_postgres_1 /bin/sh -c  "pg_dump -s -h localhost -p 5432  -U username ${DBNAME}  > /var/dump/${DBNAME}.dmp"

cp ../dump/${DBNAME}.dmp .







