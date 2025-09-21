from data.db.connection.connection import get_connection

class Core:
    def __init__(self):
        # Jadval yaratish uchun connection olish
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(200),
                name VARCHAR(200) NOT NULL,
                user_id BIGINT NOT NULL,
                channels TEXT
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
