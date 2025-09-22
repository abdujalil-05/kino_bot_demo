# from ..connection.connection import get_connection

# user_cache = []

# def add_user(username, name, user_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO users (username, name, user_id) VALUES (%s, %s, %s)",
#         (username, name, user_id)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

# def get_user(user_id):
#     if not user_cache:
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
#         data = cursor.fetchall()
#         conn.close()
#         user_cache = data
#         return data
#     return user_cache

# def user_add_channel(user_id, channel_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "UPDATE users SET channels = %s WHERE user_id = %s",
#         (str(channel_id), user_id)
#     )
#     user_cache[0][4] = channel_id
#     conn.commit()
#     cursor.close()
#     conn.close()


from ..connection.connection import get_connection

# Cache bitta global dict bo‘lishi kerak
user_cache = {}
CACHE_TTL = 3600  # 1 soat

import time

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

    # Cache yangilash
    global user_cache
    user_cache[user_id] = {"data": (username, name, user_id, None), "expires": time.time() + CACHE_TTL}


def get_user(user_id):
    global user_cache
    now = time.time()

    # Cache tekshirish
    if user_id in user_cache and user_cache[user_id]["expires"] > now:
        return user_cache[user_id]["data"]

    # DB dan olish
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if data:
        user_cache[user_id] = {"data": data, "expires": now + CACHE_TTL}

    return data


def user_add_channel(user_id, channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET channels = %s WHERE user_id = %s",
        (str(channel_id), user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Cache ham yangilanadi
    global user_cache
    if user_id in user_cache:
        user_data = list(user_cache[user_id]["data"])
        user_data[4] = str(channel_id)
        user_cache[user_id] = {"data": tuple(user_data), "expires": time.time() + CACHE_TTL}

