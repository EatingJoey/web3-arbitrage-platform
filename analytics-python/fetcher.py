# fetcher.py
import ccxt
import asyncio
import ccxt.async_support as ccxt_async
import pandas as pd
import collector as collector

def ohlcv_to_df(ohlcv, exchange_id, symbol, timeframe):
    # ohlcv: list of [timestamp, open, high, low, close, volume]
    df = pd.DataFrame(ohlcv, columns=["timestamp","open","high","low","close","volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['exchange'] = exchange_id
    df['symbol'] = symbol
    df['timeframe'] = timeframe
    collector.save_ohlcv(df,exchange_id)
    return df

def fetch_sync(exchange_id, symbol, timeframe='1h', limit=200, **kwargs):
    exchange_class = getattr(ccxt, exchange_id)
    ex = exchange_class()
    try:
        ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return ohlcv_to_df(ohlcv, exchange_id, symbol, timeframe)
    except Exception as e:
        print(f"[sync] Error fetching {exchange_id} {symbol}: {e}")
        return None
    finally:
        try:
            ex.close()
        except:
            pass

async def fetch_one_async(exchange_id, symbol, timeframe='1h', limit=200):
    ex = getattr(ccxt_async, exchange_id)()
    try:
        ohlcv = await ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return ohlcv_to_df(ohlcv, exchange_id, symbol, timeframe)
    except Exception as e:
        print(f"[async] Error fetching {exchange_id} {symbol}: {e}")
        return None
    finally:
        try:
            await ex.close()
        except:
            pass