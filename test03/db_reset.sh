
psql -h localhost -p 5432 -U username -c "drop database test03;"
psql -h localhost -p 5432 -U username -c "create database test03;"
psql -h localhost -p 5432 -U username -d test03 -f ./test03.sql
psql -h localhost -p 5432 -U username -d test03 -c "\d"

