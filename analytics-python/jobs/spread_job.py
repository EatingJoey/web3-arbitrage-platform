import time
import db

last_dex = None
last_cex = None

def get_latest_price(source, pool):
    conn = db.get_conn()
    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT price
            FROM price_records
            WHERE source=%s
            AND pool=%s
            ORDER BY id DESC
            LIMIT 1
            """,
            (source, pool)
        )
    
        row = cur.fetchone()
        conn.close()
        if row:
            return float(row[0])

    return None

def calc_spread():

    global last_dex
    global last_cex

    dex_price = get_latest_price(
        "uniswap",
        "WBTC-USDC"
    )

    cex_price = get_latest_price(
        "okx",
        "BTC/USDT"
    )

    if dex_price is None:
        return

    if cex_price is None:
        return

    spread_pct = (
        cex_price - dex_price
    ) / dex_price * 100

    print(
        f"DEX={dex_price:.2f} "
        f"CEX={cex_price:.2f} "
        f"Spread={spread_pct:.2f}%"
    )
    if (last_dex != dex_price or last_cex != cex_price):
        save_spread(dex_price,cex_price,spread_pct)
        last_dex = dex_price
        last_cex = cex_price

def save_spread(dex_price,cex_price,spread_pct):
    conn = db.get_conn()
    with conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO spread_records
            (
                symbol,
                dex_price,
                cex_price,
                spread_pct,
                ts
            )
            VALUES
            (%s,%s,%s,%s,%s)
            """,
            (
                "WBTC",
                dex_price,
                cex_price,
                spread_pct,
                int(time.time())
            )
        )

    conn.commit()

def run_spread():

    while True:

        try:

            calc_spread()

        except Exception as e:

            print(e)

        time.sleep(1)

if __name__ == "__main__":
    run_spread()