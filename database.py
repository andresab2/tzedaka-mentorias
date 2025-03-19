import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         email TEXT NOT NULL,
         phone TEXT,
         message TEXT,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def save_contact(name, email, phone, message):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO contacts (name, email, phone, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone, message))
    conn.commit()
    conn.close()
    return True 