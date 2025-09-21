from mysql.connector import pooling
import os

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
    # "host": "localhost",
    #         "user": "root",
    #         "password": "Aa20050309@",
    #         "database": "tarjima_kinolar_bot"
}

pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,   # limitni oshirmang
        pool_reset_session=True,
        **DB_CONFIG
)
    
def get_connection():
    return pool.get_connection()