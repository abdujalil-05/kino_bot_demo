from ..connection.connection import get_connection

def get_bot_admins():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bot_admins")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def add_admin(admin_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE user_id = %s", (admin_id,)
    )
    admin = cursor.fetchall()
    print(f"{admin}            admin")
    if admin:
        cursor.execute(
            "INSERT INTO bot_admins (name, admin_id, username) VALUES (%s, %s, %s)",
            (admin[0][2], admin[0][3], admin[0][1])
        )
        
        print(f"{cursor.lastrowid}        new admin")
        data = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return data
    

    conn.commit()
    cursor.close()
    conn.close()

def delete_admin(admin_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM bot_admins WHERE admin_id = %s",
        (admin_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
