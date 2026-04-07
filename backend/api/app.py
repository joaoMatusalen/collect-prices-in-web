import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Adds the root directory to sys.path so we can import from app.database if needed
# But for the API, it's safer to query directly or use a shared module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, group_name, created_at FROM products ORDER BY group_name")
                products = cur.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<int:product_id>', methods=['GET'])
def get_price_history(product_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get the price history joined with store names
                cur.execute("""
                    SELECT ph.id, ph.price, ph.url, ph.scraped_at, s.name as store_name
                    FROM price_history ph
                    JOIN stores s ON ph.store_id = s.id
                    WHERE ph.product_id = %s
                    ORDER BY ph.scraped_at ASC
                """, (product_id,))
                history = cur.fetchall()
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
