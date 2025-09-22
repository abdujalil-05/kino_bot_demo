from ..connection.connection import get_connection
import time

_channels_cache = None
_channels_cache_time = 0
CACHE_TTL = 3600  # 1 soat (sekundlarda)

def add_channel(channel_link, name, channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO channels (channels, name, channel_id) VALUES (%s, %s, %s)",
        (channel_link, name, channel_id)
    )
    conn.commit()
    cursor.close()
    conn.close()




def get_channels():
    global _channels_cache, _channels_cache_time
    now = time.time()
    
    # Agar cache bor va muddati tugamagan bo‘lsa → qaytaramiz
    if _channels_cache and now - _channels_cache_time < CACHE_TTL:
        return _channels_cache
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM channels")
        data = cursor.fetchall()
        _channels_cache = data
        _channels_cache_time = now
        return data
    finally:
        cursor.close()
        conn.close()



# def get_channels():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM channels")
#     data = cursor.fetchall()
    
#     cursor.close()
#     conn.close()
#     return data

def delete_channel(channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"DELETE FROM channels WHERE channel_id = {channel_id}",
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_user_left_channel(user_id, channels):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET channels = %s WHERE user_id = %s",
        (channels, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def add_bot_channel(channel_name, channel_id, username, channel_users_count):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bot_in_channels (channel_name, channel_id, username, channel_users_count) VALUES (%s, %s, %s, %s)",
        (channel_name, channel_id, username, channel_users_count)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_bot_channels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bot_in_channels")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def update_channel_users(channel_id, count):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bot_in_channels SET channel_users_count = %s WHERE channel_id = %s",
        (count, channel_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
