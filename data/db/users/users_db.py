from ..connection.connection import get_connection

import time
import json
import ast

user_cache = {}
CACHE_TTL = 3600

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

def add_user(username, name, user_id):
    """Yangi user qo‘shadi va cache’ni yangilaydi."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, name, user_id, channels) VALUES (%s, %s, %s, %s)",
            (username, name, user_id, None)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    
    # DB formatiga mos qilib tuple yasaymiz
    fake_row = [(None, username, name, user_id, None)]
    user_cache[user_id] = {"data": fake_row, "expires": time.time() + CACHE_TTL}


def get_user(user_id):

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

def user_add_channel(user_id, channel_id):
    """User channels ni yangilaydi (DB + cache)."""

    data = get_user(user_id)
    if not data:
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET channels = %s WHERE user_id = %s",
            (str(channel_id), user_id)
        )
        user_cache[user_id] = {"data": [(None, data[0][1], data[0][1], user_id, channel_id)], "expires": time.time() + CACHE_TTL}
        conn.commit()
    finally:
        cursor.close()
        conn.close()