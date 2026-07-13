import time

from fetcher import fetch_sync
from collector import save_ohlcv

from config import EXCHANGES
from config import SYMBOLS
from config import TIMEFRAME

INTERVAL = 60      # 每60秒检查一次


def fetch_history():
    print("loading history...")
    for ex in EXCHANGES:
        for symbol in SYMBOLS.get(ex, []):
            df = fetch_sync(
                ex,
                symbol,
                timeframe=TIMEFRAME,
                limit=500
            )
            if df is not None:
                save_ohlcv(df, ex)
                print(
                    f"{ex} {symbol} "
                    f"{len(df)} rows"
                )


def update_latest():
    for ex in EXCHANGES:
        for symbol in SYMBOLS.get(ex, []):
            df = fetch_sync(
                ex,
                symbol,
                timeframe=TIMEFRAME,
                limit=2
            )
            if df is not None:
                save_ohlcv(df, ex)


def run_fetch_job():
    print("fetch job started")
    #
    # 第一次补历史
    #
    fetch_history()
    #
    # 后面一直更新
    #
    while True:
        try:
            update_latest()
        except Exception as e:
            print(e)
        time.sleep(INTERVAL)