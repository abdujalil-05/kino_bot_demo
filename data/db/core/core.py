from mysql.connector import pooling
import os

class Core:
    def __init__(self):
        DB_CONFIG = {
            "host": os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": os.getenv("MYSQL_DATABASE"),
            "port": int(os.getenv("MYSQL_PORT", 3306))
        }

        # Connection pool yaratish
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=20,   # pooldagi maksimal connection soni
            pool_reset_session=True,
            **DB_CONFIG
        )

        # Jadval yaratish uchun connection olish
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(200),
                name VARCHAR(200) NOT NULL,
                user_id BIGINT NOT NULL,
                subscription TEXT
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS channels (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                channels VARCHAR(200) NOT NULL,
                name VARCHAR(200) NOT NULL,
                channel_id BIGINT NOT NULL
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS bot_in_channels (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                channel_name VARCHAR(200) NOT NULL,
                channel_id BIGINT NOT NULL,
                username VARCHAR(200),
                channel_users_count BIGINT NOT NULL
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS bot_admins (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                admin_id BIGINT NOT NULL,
                username VARCHAR(200)
            )
            '''
        )
        conn.commit()
        cursor.close()
        conn.close()

    # Helper method: pool'dan connection olish
    def get_connection(self):
        return self.pool.get_connection()
