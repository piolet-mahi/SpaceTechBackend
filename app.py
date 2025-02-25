from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            section TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to SpaceTech Backend API"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    name = data.get('name')
    department = data.get('department')
    year = data.get('year')
    section = data.get('section')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, department, year, section, password) VALUES (?, ?, ?, ?, ?)",
                   (name, department, year, section, password))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    name = data.get('name')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = name
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
