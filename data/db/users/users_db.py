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
#     global user_cache
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
#     global user_cache
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


# data/db/users/users_db.py
import json
import ast
import time
from ..connection.connection import get_connection

# CACHE
user_cache = {}   # {user_id: {"data": [(id, username, name, user_id, channels)], "expires": ts}}
CACHE_TTL = 3600  # 1 soat

def _parse_channels(channels_str):
    """channels ustunini string -> list aylantiradi"""
    if not channels_str:
        return []
    try:
        return json.loads(channels_str)
    except Exception:
        try:
            return ast.literal_eval(channels_str)
        except Exception:
            return []

def get_user(user_id):
    """Userni cache yoki DB dan qaytaradi (list[tuple] ko‘rinishda)."""
    now = time.time()

    # cache tekshir
    cached = user_cache.get(user_id)
    if cached and cached["expires"] > now:
        return cached["data"]

    # DB dan o‘qish
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        data = cursor.fetchall()   # [(id, username, name, user_id, channels)]
    finally:
        cursor.close()
        conn.close()

    if data:
        user_cache[user_id] = {"data": data, "expires": now + CACHE_TTL}

    return data

def add_user(username, name, user_id):
    """Yangi user qo‘shadi va cache’ni yangilaydi."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, name, user_id, channels) VALUES (%s, %s, %s, %s)",
            (username, name, user_id, "[]")
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    # DB formatiga mos qilib tuple yasaymiz
    fake_row = [(None, username, name, user_id, "[]")]
    user_cache[user_id] = {"data": fake_row, "expires": time.time() + CACHE_TTL}

def user_add_channel(user_id, channel_id):
    """User channels ni yangilaydi (DB + cache)."""
    data = get_user(user_id)
    if not data:
        return

    row = data[0]
    channels_list = _parse_channels(row[4])
    ch = str(channel_id)
    if ch not in channels_list:
        channels_list.append(ch)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET channels = %s WHERE user_id = %s",
                (json.dumps(channels_list), user_id)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        # cache yangilash
        updated_row = (row[0], row[1], row[2], row[3], json.dumps(channels_list))
        user_cache[user_id] = {"data": [updated_row], "expires": time.time() + CACHE_TTL}

def user_remove_channel(user_id, channel_id):
    """Userdan kanalni olib tashlaydi."""
    data = get_user(user_id)
    if not data:
        return

    row = data[0]
    channels_list = _parse_channels(row[4])
    ch = str(channel_id)
    if ch in channels_list:
        channels_list.remove(ch)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET channels = %s WHERE user_id = %s",
                (json.dumps(channels_list), user_id)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        updated_row = (row[0], row[1], row[2], row[3], json.dumps(channels_list))
        user_cache[user_id] = {"data": [updated_row], "expires": time.time() + CACHE_TTL}

def invalidate_user_cache(user_id):
    """Cache tozalash."""
    user_cache.pop(user_id, None)
