if [ $# -eq 1 ];then
   DBNAME=$1
else  
   DBNAME=`./get_dbname.sh`
fi
echo ${DBNAME}
echo \#DATABASE
psql -h localhost -p 5432 -U username  -P pager=off  -c "\l"
echo \#TABLE 
psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off  -c "\d"
psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off  -c "\ds+"

echo \#TABLE pg_sequence
psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off  -c "TABLE pg_sequence;"

SQL="SELECT c.relname,t.typname, s.*  \
  FROM pg_sequence as s, pg_class as c, pg_type t \
  WHERE s.seqrelid = c.oid AND s.seqtypid = t.oid;"

psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off  -c "$SQL"

