from datetime import datetime
import os
import requests
import time
import pymysql
import db
import logging

logger = logging.getLogger(__name__)

def collect_prices(interval=1):
    api = os.getenv("API_URL")
    while True:
        try:
            data = requests.get(f"{api}/prices", timeout=3).json()
            for item in data:
                save_price(item)

            #print(f"collect: {data}")

            time.sleep(interval)
            
        except Exception  as e:
            logger.warning(f"Collector unavailable: {e}")
            time.sleep(2)



def save_price(item):
    conn = db.get_conn()
    with conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO price_records
            (source,pool, price, ts)
            VALUES (%s,%s,%s,%s)
            """,
            (
                "uniswap",
                item["pool"],
                item["price"],
                #datetime.fromtimestamp(item["timestamp"])
                item["timestamp"]
            )
        )

    conn.commit()

def save_ohlcv(df,source):
    conn = db.get_conn()
    values = [
    (source, row['symbol'], float(row["close"]), int(row['timestamp'].timestamp()))
    for _, row in df.iterrows()]
    with conn.cursor() as cur:
        cur.executemany(
        """INSERT IGNORE INTO price_records (source,pool,price,ts) VALUES (%s,%s,%s,%s)""",
        values)
    conn.commit()
    conn.close()