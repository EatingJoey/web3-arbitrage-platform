# 配置需要的交易所与市场对
EXCHANGES = ["okx","binance","bybit"]  # ccxt 的交易所 id，okx 对应 ccxt 中是 "okx"
SYMBOLS = {
    "okx":     ["BTC/USDT", "ETH/USDT"],
    "binance": ["BTC/USDT", "ETH/USDT"],
    "bybit":   ["BTC/USDT", "ETH/USDT"]
}
TIMEFRAME = "1h"   # k线周期
LIMIT = 200        # 拉取多少根k线
ENTRY_Z = -2
EXIT_Z = 0
FEE = 0.001      # 0.1%
STOP_LOSS = -0.5
TAKE_PROFIT = 0.8