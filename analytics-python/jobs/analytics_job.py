import pandas as pd
import time
import db

def load_spread(limit=200):
    conn = db.get_conn()

    try:
        sql = """
        SELECT
            symbol,
            spread_pct,
            ts
        FROM spread_records
        ORDER BY id DESC
        LIMIT %s
        """

        df = pd.read_sql(sql, conn, params=[limit])
        return df

    finally:
        conn.close()


# ========= 计算指标 =========
def compute_indicators(df):

    # 按时间正序（非常重要）
    df = df.sort_values("ts").reset_index(drop=True)

    # MA
    df["ma20"] = df["spread_pct"].rolling(20).mean()
    df["ma60"] = df["spread_pct"].rolling(60).mean()

    # STD
    df["std20"] = df["spread_pct"].rolling(20).std()

    # Z-score（防止除0）
    df["zscore"] = (df["spread_pct"] - df["ma20"]) / df["std20"]
    df["zscore"] = df["zscore"].fillna(0)

    return df


# ========= 写入 analytics =========
def save_latest(row):

    conn = db.get_conn()

    try:
        with conn.cursor() as cur:

            sql = """
            INSERT INTO analytics_records
            (symbol, spread, ma20, ma60, std20, zscore, ts)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """

            cur.execute(sql, (
                row["symbol"],
                float(row["spread_pct"]),
                float(row["ma20"]),
                float(row["ma60"]) if pd.notna(row["ma60"]) else 0,
                float(row["std20"]) if pd.notna(row["std20"]) else 0,
                float(row["zscore"]),
                int(row["ts"])
            ))

            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


# ========= 主循环 =========
def run_analytics():
    print("analytics job started...")

    last_ts = None

    while True:

        try:

            df = load_spread(200)

            if df.empty:
                time.sleep(1)
                continue

            df = compute_indicators(df)

            latest = df.iloc[-1]

            # 防重复写入
            if last_ts != latest["ts"]:
                save_latest(latest)
                last_ts = latest["ts"]

                print(
                    f"[ANALYTICS] spread={latest['spread_pct']:.4f} "
                    f"ma20={latest['ma20']:.4f} "
                    f"zscore={latest['zscore']:.2f}"
                )

        except Exception as e:
            print("[ERROR]", e)

        time.sleep(1)


if __name__ == "__main__":
    run_analytics()