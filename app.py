
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS service_records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 name TEXT, 
                 date TEXT, 
                 status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    records = conn.execute('SELECT * FROM service_records').fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    date = request.form['date']
    status = request.form['status']
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO service_records (name, date, status) VALUES (?, ?, ?)", (name, date, status))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
