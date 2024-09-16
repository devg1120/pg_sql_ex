#DBNAME=ramen_shop
#echo -n "dbname:" > ./_env_
#echo ${DBNAME} >> ./_env_
DBNAME=`./get_dbname.sh`
psql -h localhost -p 5432 -U username -c "drop database IF EXISTS ${DBNAME};"
psql -h localhost -p 5432 -U username -c "create database ${DBNAME};"
psql -h localhost -p 5432 -U username -d ${DBNAME} -f ./test.sql
psql -h localhost -p 5432 -U username -d ${DBNAME} -c "\d"

