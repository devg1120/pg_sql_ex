
POSTGRES_VERSION=14.3
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=username
POSTGRES_DB=test01

docker run -v "$(pwd):/dump" -it --rm --network host postgres:${POSTGRES_VERSION} pg_dump -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -v -s -f /dump/database.dump  -W

