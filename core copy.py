import mysql.connector

class Core:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'chat_db'
        )

        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(32) NOT NULL,
            password VARCHAR(32) NOT NULL
        )''')
        cursor.close()

    def insert_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute(
            f"""INSERT INTO users (username, password) 
            VALUES ("{username}", "{password}")"""
        )
        cursor.close()
        self.connection.commit()
        self.connection.close()

    def get_users(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT username, password FROM users""")
        data = cursor.fetchall()
        return data


# core = Core()
# # core.insert_user("aziza", '12324')
# core.get_users()