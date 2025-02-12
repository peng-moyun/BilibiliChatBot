# user_data_manager.py

import sqlite3
from datetime import datetime

# 创建数据库和表
def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_messages (
        uid INTEGER PRIMARY KEY,
        message_count INTEGER,
        last_updated TEXT
    )
    ''')
    conn.commit()
    conn.close()

# 每日重置消息计数
def reset_daily_message_count():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE user_messages SET message_count = 0, last_updated = ?', (datetime.now().date(),))
    conn.commit()
    conn.close()
    print("Daily message counts have been reset.")

# 手动清除指定用户的 message_count
def clear_user_message_count(uid):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE user_messages SET message_count = 0 WHERE uid = ?', (uid,))
        conn.commit()
        print(f"Message count for user {uid} has been cleared.")
    except Exception as e:
        print(f"Error clearing message count for user {uid}: {e}")
    finally:
        conn.close()

# 初始化数据库
init_db()
