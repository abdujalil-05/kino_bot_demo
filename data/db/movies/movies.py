from ..connection.connection import get_connection


def add_movie(movie_name, movie_year, movie_language, genres, url, description, rating):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO movies (movie_name, movie_year, movie_language, genres, url, description, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (movie_name, movie_year, movie_language, genres, url, description, rating)
    )

    last_id = cursor.lastrowid
    conn.commit()

    cursor.execute(
        """
        INSERT INTO items (is_movie, is_season, movie_id, episode_id)
        VALUES (%s, %s, %s, %s)
        """, (True, False, last_id, None)
    )
    last_id = cursor.lastrowid
    conn.commit()
    cursor.close()

    return last_id



def get_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM items WHERE id = %s", (movie_id,)
    )
    movie_item = cursor.fetchall()
    if movie_item != []:
        if movie_item[0][1]:
            movie_code = movie_item[0][3]
            cursor.execute(
                "SELECT * FROM movies WHERE id = %s", (movie_code,)
            )
            data = cursor.fetchall()
            data.append({
                "is_movie": True
            })
            return data
        else:
            episode_code = movie_item[0][4]
            cursor.execute(
                "SELECT * FROM episodes WHERE id = %s", (episode_code,)
            )
            data = cursor.fetchall()
            data.append({
                "is_movie": False
            })
            return data
    cursor.close()
    conn.close()
    return []
    
    


def delete_movie(movie_code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM items WHERE id = %s", (movie_code,)
    )
    movie_id = cursor.fetchall()
    if movie_id:
        cursor.execute(
            "DELETE FROM movies WHERE id = %s", (movie_id[0][3],)
        )
        cursor.execute(
            "DELETE FROM items WHERE id = %s", (movie_code,)
        )
        conn.commit()
        cursor.execute(
            "SELECT * FROM items WHERE id = %s", (movie_code,)
        )
        data_item = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM movies WHERE id = %s", (movie_id[0][3],)
        )  
        data_movie = cursor.fetchall()
        if data_item == data_movie:
            return True
    cursor.close()
    conn.close()
    return False      


