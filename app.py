from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'database.db'

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS service_records
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      date TEXT,
                      status TEXT)''')
        conn.commit()
        conn.close()

@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    records = conn.execute('SELECT * FROM service_records').fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    date = request.form['date']
    status = request.form['status']
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO service_records (name, date, status) VALUES (?, ?, ?)", (name, date, status))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
