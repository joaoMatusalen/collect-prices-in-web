from flask import Blueprint, jsonify

from api.db import get_db_connection

stores_bp = Blueprint('stores', __name__)


@stores_bp.route('/api/stores', methods=['GET'])
def get_stores():
    """List all stores."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM stores ORDER BY name")
                stores = cur.fetchall()
        return jsonify(stores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
