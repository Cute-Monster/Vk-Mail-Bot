if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect("db/bot.db")
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM SeenMessages
    """)
    conn.commit()
    cursor.execute("""
    SELECT mess_text FROM SeenMessages
    """)
    print(cursor.fetchone())
    conn.close()

