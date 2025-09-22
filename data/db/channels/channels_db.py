# from ..connection.connection import get_connection
# import time

# _channels_cache = None
# _channels_cache_time = 0
# CACHE_TTL = 3600  # 1 soat (sekundlarda)

# def add_channel(channel_link, name, channel_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO channels (channels, name, channel_id) VALUES (%s, %s, %s)",
#         (channel_link, name, channel_id)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()




# def get_channels():
#     global _channels_cache, _channels_cache_time
#     now = time.time()
    
#     # Agar cache bor va muddati tugamagan bo‘lsa → qaytaramiz
#     if _channels_cache and now - _channels_cache_time < CACHE_TTL:
#         return _channels_cache
    
#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("SELECT * FROM channels")
#         data = cursor.fetchall()
#         _channels_cache = data
#         _channels_cache_time = now
#         return data
#     finally:
#         cursor.close()
#         conn.close()



# # def get_channels():
# #     conn = get_connection()
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT * FROM channels")
# #     data = cursor.fetchall()
    
# #     cursor.close()
# #     conn.close()
# #     return data

# def delete_channel(channel_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         f"DELETE FROM channels WHERE channel_id = {channel_id}",
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

# def delete_user_left_channel(user_id, channels):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         f"UPDATE users SET channels = %s WHERE user_id = %s",
#         (channels, user_id)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

# def add_bot_channel(channel_name, channel_id, username, channel_users_count):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO bot_in_channels (channel_name, channel_id, username, channel_users_count) VALUES (%s, %s, %s, %s)",
#         (channel_name, channel_id, username, channel_users_count)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

# def get_bot_channels():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM bot_in_channels")
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return data

# def update_channel_users(channel_id, count):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "UPDATE bot_in_channels SET channel_users_count = %s WHERE channel_id = %s",
#         (count, channel_id)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()



from ..connection.connection import get_connection
import time

# Global cachelar
_channels_cache = None
_channels_cache_time = 0

_bot_channels_cache = None
_bot_channels_cache_time = 0

CACHE_TTL = 3600  # 1 soat (sekundlarda)


def add_channel(channel_link, name, channel_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO channels (channels, name, channel_id) VALUES (%s, %s, %s)",
                (channel_link, name, channel_id)
            )
        conn.commit()

    # Cache yangilanadi
    global _channels_cache, _channels_cache_time
    _channels_cache = None
    _channels_cache_time = 0


def get_channels():
    global _channels_cache, _channels_cache_time
    now = time.time()

    if _channels_cache and now - _channels_cache_time < CACHE_TTL:
        return _channels_cache

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM channels")
            data = cursor.fetchall()

    _channels_cache = data
    _channels_cache_time = now
    return data


def delete_channel(channel_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM channels WHERE channel_id = %s",
                (channel_id,)
            )
        conn.commit()

    # Cache yangilanadi
    global _channels_cache, _channels_cache_time
    _channels_cache = None
    _channels_cache_time = 0


def delete_user_left_channel(user_id, channels):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET channels = %s WHERE user_id = %s",
                (channels, user_id)
            )
        conn.commit()


def add_bot_channel(channel_name, channel_id, username, channel_users_count):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO bot_in_channels (channel_name, channel_id, username, channel_users_count) VALUES (%s, %s, %s, %s)",
                (channel_name, channel_id, username, channel_users_count)
            )
        conn.commit()

    # Cache yangilanadi
    global _bot_channels_cache, _bot_channels_cache_time
    _bot_channels_cache = None
    _bot_channels_cache_time = 0


def get_bot_channels():
    global _bot_channels_cache, _bot_channels_cache_time
    now = time.time()

    if _bot_channels_cache and now - _bot_channels_cache_time < CACHE_TTL:
        return _bot_channels_cache

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bot_in_channels")
            data = cursor.fetchall()

    _bot_channels_cache = data
    _bot_channels_cache_time = now
    return data


def update_channel_users(channel_id, count):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE bot_in_channels SET channel_users_count = %s WHERE channel_id = %s",
                (count, channel_id)
            )
        conn.commit()

    # Cache yangilanadi
    global _bot_channels_cache, _bot_channels_cache_time
    _bot_channels_cache = None
    _bot_channels_cache_time = 0


