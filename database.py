import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('loans.db')
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                total_amount REAL NOT NULL,
                installments INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_loan(self, name, phone, total_amount, installments):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO loans (name, phone, total_amount, installments)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, total_amount, installments))
        self.conn.commit()
    
    def get_all_loans(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM loans')
        return cursor.fetchall()
    
    def update_loan(self, id, name, phone, total_amount, installments):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE loans 
            SET name=?, phone=?, total_amount=?, installments=?
            WHERE id=?
        ''', (name, phone, total_amount, installments, id))
        self.conn.commit()
    
    def get_loan(self, id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM loans WHERE id=?', (id,))
        return cursor.fetchone()