
psql -h localhost -p 5432 -U username -c "drop database test01;"
psql -h localhost -p 5432 -U username -c "create database test01;"
psql -h localhost -p 5432 -U username -d test01 -f ./test01.sql
psql -h localhost -p 5432 -U username -d test01 -c "\d"

