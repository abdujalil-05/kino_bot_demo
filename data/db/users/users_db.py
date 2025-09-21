from ..core.core import Core

core = Core()

def add_user(username, name, user_id):
    conn = core.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, name, user_id) VALUES (%s, %s, %s)",
        (username, name, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_user(user_id):
    conn = core.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def user_add_channel(user_id, channel_id):
    conn = core.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET channels = %s WHERE user_id = %s",
        (str(channel_id), user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
