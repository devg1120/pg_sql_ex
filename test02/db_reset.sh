DBNAME=test02
echo -n "dbname:" > ./_dbname_
echo ${DBNAME} > ./_dbname_
psql -h localhost -p 5432 -U username -c "drop database ${DBNAME};"
psql -h localhost -p 5432 -U username -c "create database ${DBNAME};"
psql -h localhost -p 5432 -U username -d ${DBNAME} -f ./test.sql
psql -h localhost -p 5432 -U username -d ${DBNAME} -c "\d"

