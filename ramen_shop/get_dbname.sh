
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
		   #echo "*dbname:" ${ARR[1]};
		   DBNAME=${ARR[1]};;
	   "username")
		   #echo "*username:" ${ARR[1]};;
		   echo -n "";;
            *)
		   #echo "...unknow:" ${ARR[0]};;
		   echo -n "";;
   esac

   IFS=$'\n'

done
echo $DBNAME

