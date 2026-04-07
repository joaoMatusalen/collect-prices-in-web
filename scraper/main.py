from app.database import create_tables, save_result
from app.runner import run

create_tables()

def get_products_to_scrape(conn) -> dict:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.group_name, pu.url
            FROM product_urls pu
            JOIN products p ON p.id = pu.product_id
            WHERE pu.active = TRUE
        """)
        rows = cur.fetchall()

    products = {}
    for group_name, url in rows:
        products.setdefault(group_name, []).append(url)
    return products

results = run(products)

for result in results:
    save_result(result)

print(f"\nTotal salvo: {len(results)} registros")