import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self, db_path='data/scraped_posts.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()
    
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                likes INTEGER,
                comments INTEGER,
                shares INTEGER,
                hashtags TEXT,
                post_time DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                post_id INTEGER PRIMARY KEY,
                positive INTEGER DEFAULT 0,
                negative INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def log_feedback(self, post_id, is_positive):
        cursor = self.conn.cursor()
        cursor.execute('SELECT positive, negative FROM feedback WHERE post_id = ?', (post_id,))
        row = cursor.fetchone()
        if row:
            positive, negative = row
            if is_positive:
                positive += 1
            else:
                negative += 1
            cursor.execute('UPDATE feedback SET positive = ?, negative = ? WHERE post_id = ?', (positive, negative, post_id))
        else:
            positive = 1 if is_positive else 0
            negative = 0 if is_positive else 1
            cursor.execute('INSERT INTO feedback (post_id, positive, negative) VALUES (?, ?, ?)', (post_id, positive, negative))
        self.conn.commit()
