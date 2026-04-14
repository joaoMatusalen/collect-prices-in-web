from flask import Blueprint, jsonify, request

from api.db import get_db_connection

analytics_bp = Blueprint('analytics', __name__)


def _empty_analytics_payload(store_stats=None):
    return {
        "filteredData": [],
        "overallStats": {
            "current": None,
            "currentStore": None,
            "min": None,
            "minStore": None,
            "max": None,
            "maxStore": None,
            "avg": None,
        },
        "storeStats": store_stats or [],
    }


@analytics_bp.route('/api/analytics/<int:product_id>', methods=['GET'])
def get_product_analytics(product_id):
    """Return the price history, overall stats, and store stats for a product."""
    try:
        days = request.args.get('days', '30')

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                date_filter = ""
                params = [product_id]

                if days != 'all':
                    try:
                        days_int = int(days)
                        # We use PostgreSQL intervals for precision.
                        date_filter = "AND ph.scraped_at >= NOW() - INTERVAL '%s days'"
                        params.append(days_int)
                    except ValueError:
                        pass

                query = f"""
                    SELECT ph.id, ph.price, ph.url, ph.scraped_at, s.name as store_name
                    FROM price_history ph
                    JOIN stores s ON ph.store_id = s.id
                    WHERE ph.product_id = %s {date_filter}
                    ORDER BY ph.scraped_at ASC
                """

                cur.execute(query, tuple(params))
                history = cur.fetchall()

                if not history:
                    return jsonify(_empty_analytics_payload())

                store_map = {}
                for item in history:
                    store = item['store_name'] or 'Loja'
                    store_map.setdefault(store, []).append(item)

                store_stats = []
                for store, items in store_map.items():
                    store_prices = [float(entry['price']) for entry in items]
                    latest = items[-1]
                    store_stats.append({
                        "storeName": store,
                        "min": min(store_prices),
                        "max": max(store_prices),
                        "avg": sum(store_prices) / len(store_prices),
                        "samples": len(items),
                        "latestPrice": float(latest['price']),
                        "latestUrl": latest['url'],
                        "latestScrapedAt": latest['scraped_at'],
                    })

                store_stats.sort(key=lambda item: item["storeName"])

                store_filter = request.args.get('store', 'all')
                if store_filter != 'all':
                    history_for_stats = [item for item in history if item['store_name'] == store_filter]
                else:
                    history_for_stats = history

                if not history_for_stats:
                    return jsonify(_empty_analytics_payload(store_stats))

                prices = [float(item['price']) for item in history_for_stats]
                min_idx = prices.index(min(prices))
                max_idx = prices.index(max(prices))

                filtered_store_map = {}
                for item in history_for_stats:
                    store = item['store_name'] or 'Loja'
                    filtered_store_map.setdefault(store, []).append(item)

                latest_prices = []
                for store, items in filtered_store_map.items():
                    latest = items[-1]
                    latest_prices.append({
                        "store": store,
                        "price": float(latest['price']),
                    })

                best_latest = min(latest_prices, key=lambda item: item["price"])

                overall_stats = {
                    "current": best_latest["price"],
                    "currentStore": best_latest["store"],
                    "min": prices[min_idx],
                    "minStore": history_for_stats[min_idx]['store_name'],
                    "max": prices[max_idx],
                    "maxStore": history_for_stats[max_idx]['store_name'],
                    "avg": sum(prices) / len(prices),
                }

                return jsonify({
                    "filteredData": history_for_stats,
                    "overallStats": overall_stats,
                    "storeStats": store_stats,
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
