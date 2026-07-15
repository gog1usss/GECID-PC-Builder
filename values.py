import pymysql

SECRET_KEY = "GECID_SUPER_PUPER_PASS_Ladowka"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 25


DB_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'sqladmin',
    'database': 'gecid_pc',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
