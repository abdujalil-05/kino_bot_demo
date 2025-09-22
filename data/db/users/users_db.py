from ..connection.connection import get_connection

user_cache = []

def add_user(username, name, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, name, user_id) VALUES (%s, %s, %s)",
        (username, name, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_user(user_id):
    if not user_cache:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        data = cursor.fetchall()
        conn.close()
        user_cache = data
        return data
    return user_cache

def user_add_channel(user_id, channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET channels = %s WHERE user_id = %s",
        (str(channel_id), user_id)
    )
    user_cache[0][4] = channel_id
    conn.commit()
    cursor.close()
    conn.close()
