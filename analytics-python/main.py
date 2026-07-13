# main.py
import threading
from config import EXCHANGES, SYMBOLS, TIMEFRAME, LIMIT
from fetcher import fetch_sync, fetch_one_async
from visualizer import plot_candles, plot_close_compare
import asyncio
from collector import collect_prices
from jobs.spread_job import run_spread
from jobs.analytics_job import run_analytics
from jobs.fetch_job import run_fetch_job
import warnings

warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy"
)

def run_sync_demo():
    import pandas as pd
    frames = []
    for ex in EXCHANGES:
        for s in SYMBOLS.get(ex, []):
            df = fetch_sync(ex, s, timeframe=TIMEFRAME, limit=LIMIT)
            if df is not None:
                frames.append(df)
    if frames:
        df_all = pd.concat(frames, ignore_index=True)
        # 示例：绘制币安 BTC/USDT 烛台
        df_btc = df_all[(df_all['exchange']=='binance') & (df_all['symbol']=='BTC/USDT')]
        if not df_btc.empty:
            plot_candles(df_btc, 'binance', 'BTC/USDT')
        # 比较不同交易所 BTC/USDT 收盘价
        plot_close_compare(df_all, 'BTC/USDT')

def run_async_demo():
    df_all = asyncio.run(fetch_one_async('binance','BTC/USDT', timeframe=TIMEFRAME, limit=LIMIT))
    if not df_all.empty:
        plot_close_compare(df_all, 'BTC/USDT')
        # 单交易所单symbol
        df_btc = df_all[(df_all['exchange']=='okx') & (df_all['symbol']=='BTC/USDT')]
        if not df_btc.empty:
            plot_candles(df_btc, 'okx', 'BTC/USDT')

if __name__ == "__main__":
    # 运行异步示例（更高效）
    #run_async_demo()
    # 或者运行同步示例
    #collect_prices()
    #run_sync_demo()
        # 创建两个线程并行执行
    t1 = threading.Thread(target=collect_prices, daemon=True)
    t2 = threading.Thread(target=run_fetch_job, daemon=True)
    t3 = threading.Thread(target=run_spread,daemon=True)
    t4 = threading.Thread(target=run_analytics,daemon=True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    # 主线程等待两个线程
    t1.join()
    t2.join()
    t3.join()
    t4.join()
