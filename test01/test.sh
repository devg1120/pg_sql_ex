
HOST=""
DBNAME=""
USERBANE=""
PASSWORD=""

ORGIFS=${IFS}
IFS=$'\n'
for LINE in `cat ./_env_`
do
   #echo $LINE
   IFS=${ORGIFS}

   line_head="${LINE:0:1}"
   if [ "$line_head" == "#" ]; then
	   continue
   fi
   if [ "$line_head" == " " ]; then
	   continue
   fi

   ARR=(${LINE//:/ })
   #echo ${ARR[0]}
   case ${ARR[0]} in
	   "dbname")
		   echo "*dbname:" ${ARR[1]};
		   DBNAME=${ARR[1]};;
	   "username")
		   echo "*username:" ${ARR[1]};;
            *)
		   echo "...unknow:" ${ARR[0]};;
   esac

   IFS=$'\n'

done
echo $DBNAME
#psql -h localhost -p 5432 -U username -d ${DBNAME} -c "\dt"
#psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off -c "\d users"
#psql -h localhost -p 5432 -U username -d ${DBNAME} -P pager=off -c "select * from users ;"
python3 print_table.py

