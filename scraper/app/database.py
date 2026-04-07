import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def create_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name TEXT,
        group_name TEXT,
        url TEXT NOT NULL,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        UNIQUE (url)
    );

    CREATE TABLE IF NOT EXISTS stores (
        id    SERIAL PRIMARY KEY,
        name  TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS price_history (
        price_history_id SERIAL PRIMARY KEY,
        product_id  INT REFERENCES products(id),
        store_id    INT REFERENCES stores(id),
        price       NUMERIC(12, 2) NOT NULL,
        url         TEXT,
        scraped_at  TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_price_history_lookup
        ON price_history(product_id, scraped_at DESC);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def get_or_create_store(conn, store_name: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO stores (name) VALUES (%s)"
            " ON CONFLICT (name) DO NOTHING",
            (store_name,)
        )
        cur.execute(
            "SELECT id FROM stores WHERE name = %s",
            (store_name,)
        )
        return cur.fetchone()[0]


def save_result(result: dict):
    with get_connection() as conn:
        product_id = get_or_create_product(conn, result["product_group"])
        store_id   = get_or_create_store(conn, result["store"])

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO price_history (product_id, store_id, price, url, scraped_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    product_id,
                    store_id,
                    result["price"],
                    result["url"],
                    result["scraped_at"],
                )
            )