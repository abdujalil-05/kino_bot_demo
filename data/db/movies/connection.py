from mysql.connector import pooling
import os

class MoviesDb:
    def __init__(self):
        DB_CONFIG = {
            "host": os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": os.getenv("MYSQL_DATABASE"),
            "port": int(os.getenv("MYSQL_PORT", 3306))
        }

        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=20,
            pool_reset_session=True,
            **DB_CONFIG
        )


        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                movie_name VARCHAR(200) NOT NULL,
                movie_year VARCHAR(32) NOT NULL,
                movie_language VARCHAR(32) NOT NULL,
                genres TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT NOT NULL,
                rating VARCHAR(32) NOT NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS seasons (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                season_name VARCHAR(200) NOT NULL,
                season_year VARCHAR(32) NOT NULL,
                season_episode_count INT,
                description TEXT NOT NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS episodes (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                episode_name VARCHAR(200) NOT NULL,
                episode_year VARCHAR(32) NOT NULL,
                episode_language VARCHAR(32) NOT NULL,
                genres TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT NOT NULL,
                season_id INT NOT NULL,
                FOREIGN KEY (season_id) REFERENCES seasons(id) ON DELETE CASCADE
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                is_movie BOOLEAN DEFAULT FALSE,
                is_season BOOLEAN DEFAULT FALSE,
                movie_id INT DEFAULT NULL,
                episode_id INT DEFAULT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
                FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
            );
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_connection(self):
        return self.pool.get_connection()
