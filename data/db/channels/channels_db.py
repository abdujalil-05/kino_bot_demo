from ..connection.connection import get_connection
import time

# Global cachelar
_channels_cache = None
_channels_cache_time = 0


CACHE_TTL = 60  # 1 soat (sekundlarda)


def _invalidate_channels_cache():
    global _channels_cache, _channels_cache_time
    _channels_cache = None
    _channels_cache_time = 0


def add_channel(channel_link, name, channel_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO channels (channels, name, channel_id) VALUES (%s, %s, %s)",
                (channel_link, name, channel_id)
            )
        conn.commit()
    _invalidate_channels_cache()


def get_channels():
    global _channels_cache, _channels_cache_time
    now = time.time()

    if _channels_cache is not None and now - _channels_cache_time < CACHE_TTL:
        return _channels_cache

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM channels")
            data = cursor.fetchall()

    _channels_cache = data
    _channels_cache_time = now
    return data


def delete_channel(channel_id):
    print("a")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM channels WHERE channel_id = %s",
                (channel_id,)
            )
        conn.commit()
    _invalidate_channels_cache()


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


def get_bot_channels():
    now = time.time()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM bot_in_channels")
            data = cursor.fetchall()

    return data


def update_channel_users(channel_id, count):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE bot_in_channels SET channel_users_count = %s WHERE channel_id = %s",
                (count, channel_id)
            )
        conn.commit()