from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price TEXT NOT NULL,
                            image TEXT NOT NULL)''')

@app.route('/')
def index():
    with get_db_connection() as conn:
        products = conn.execute('SELECT * FROM products').fetchall()
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('id')
    if product_id is None:
        return jsonify({'error': 'Invalid product ID'}), 400
    return jsonify({'message': 'Product added', 'id': product_id})

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0', port=3003)
