
import sqlite3
from datetime import datetime
import os

DB_PATH = 'history.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            customer_age INTEGER,
            gender TEXT,
            dependent_count INTEGER,
            education_level TEXT,
            marital_status TEXT,
            income_category TEXT,
            card_category TEXT,
            months_on_book INTEGER,
            total_relationship_count INTEGER,
            months_inactive_12_mon INTEGER,
            contacts_count_12_mon INTEGER,
            credit_limit REAL,
            total_revolving_bal INTEGER,
            avg_open_to_buy REAL,
            total_amt_chng_q4_q1 REAL,
            total_trans_amt INTEGER,
            total_trans_ct INTEGER,
            total_ct_chng_q4_q1 REAL,
            avg_utilization_ratio REAL,
            prediction TEXT,
            confidence REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(data, result, confidence):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (
            timestamp, customer_age, gender, dependent_count, education_level,
            marital_status, income_category, card_category, months_on_book,
            total_relationship_count, months_inactive_12_mon, contacts_count_12_mon,
            credit_limit, total_revolving_bal, avg_open_to_buy, total_amt_chng_q4_q1,
            total_trans_amt, total_trans_ct, total_ct_chng_q4_q1, avg_utilization_ratio,
            prediction, confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data['customer_age'], data['gender'], data['dependent_count'], data['education_level'],
        data['marital_status'], data['income_category'], data['card_category'], data['months_on_book'],
        data['total_relationship_count'], data['months_inactive_12_mon'], data['contacts_count_12_mon'],
        data['credit_limit'], data['total_revolving_bal'], data['avg_open_to_buy'], data['total_amt_chng_q4_q1'],
        data['total_trans_amt'], data['total_trans_ct'], data['total_ct_chng_q4_q1'], data['avg_utilization_ratio'],
        result, confidence
    ))
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    
    # Convert to list of dicts
    history = []
    columns = [description[0] for description in cursor.description]
    for row in rows:
        history.append(dict(zip(columns, row)))
    
    conn.close()
    return history

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
