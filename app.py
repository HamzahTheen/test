from flask import Flask, render_template, jsonify
import sqlite3
import requests

app = Flask(__name__)

# API Keys
UNSPLASH_API_KEY = "your_unsplash_api_key"
OPENWEATHER_API_KEY = "your_openweather_api_key"

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/destinations')
def get_destinations():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, description, image_url FROM destinations')
    rows = cursor.fetchall()
    conn.close()

    destinations = [
        {"name": row[0], "description": row[1], "image": row[2]}
        for row in rows
    ]
    return jsonify(destinations)

@app.route('/populate')
def populate_db():
    destinations = [
        {"name": "Paris", "description": "City of Lights"},
        {"name": "Tokyo", "description": "Modern and traditional collide"},
        {"name": "New York", "description": "The Big Apple"},
    ]

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for dest in destinations:
        # Get image from Unsplash API
        response = requests.get(
            f"https://api.unsplash.com/search/photos?query={dest['name']}&client_id={UNSPLASH_API_KEY}"
        )
        image_url = response.json()['results'][0]['urls']['small']

        cursor.execute('''
            INSERT INTO destinations (name, description, image_url)
            VALUES (?, ?, ?)
        ''', (dest['name'], dest['description'], image_url))
    
    conn.commit()
    conn.close()
    return "Database populated!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
