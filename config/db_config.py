import psycopg2

HOST = "172.30.120.234"
PORT = "5432"
USER = "py"
PASSWD = "py"
DB = "scraper"

def get_connection():
    return psycopg2.connect(
        database = DB,
        user = USER,
        password = PASSWD,
        host = HOST,
        port = PORT
    )
