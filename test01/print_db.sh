DBNAME=`./get_dbname.sh`
echo ${DBNAME}
psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off  -c "\d"

ORGIFS=${IFS}
IFS=$'\n'
declare -a TABLES
for LINE in `psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off  -c "\d"`
do
   IFS=${ORGIFS}
   LINE=`echo $LINE`
   line_head="${LINE:0:6}"
   if [ "$line_head" == "public" ]; then
	  ARR=(${LINE//|/ })
	  TABLE_NAME=${ARR[1]}
	  TABLES+=($TABLE_NAME)
   fi
   IFS=$'\n'
done

for I in ${!TABLES[@]}; 
do
   echo "$I : [${TABLES[$I]}]"  
   TABLE=${TABLES[$I]} 
   psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off -c "select * from $TABLE;"
done

