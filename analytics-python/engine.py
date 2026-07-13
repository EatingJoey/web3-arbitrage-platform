from models import Trade
from config import *


class BacktestEngine:
    def __init__(self, strategy):
        self.strategy = strategy
        self.position = None
        self.entry_spread = None
        self.entry_time = None
        self.trades = []

    def run(self, df):
        for _, row in df.iterrows():
            signal = self.strategy.next(row)
            spread = row["spread"]
            ts = int(row["ts"])
            # --------------------------
            # 开仓
            # --------------------------
            if self.position is None:
                if signal == "BUY":
                    self.position = "LONG"
                    self.entry_spread = spread
                    self.entry_time = ts

            # --------------------------
            # 平仓
            # --------------------------
            else:
                pnl = spread - self.entry_spread
                if (
                    signal == "SELL"
                    or pnl <= STOP_LOSS
                    or pnl >= TAKE_PROFIT
                ):
                    fee = abs(self.entry_spread) * FEE
                    pnl_after_fee = pnl - fee
                    hold_seconds = ts - self.entry_time
                    trade = Trade(
                        entry_time=self.entry_time,
                        exit_time=ts,
                        entry_spread=self.entry_spread,
                        exit_spread=spread,
                        direction="LONG",
                        pnl=pnl,
                        fee=fee,
                        hold_seconds=hold_seconds,
                        pnl_after_fee=pnl_after_fee
                    )
                    self.trades.append(trade)
                    self.position = None
                    self.entry_spread = None
                    self.entry_time = None
        return self.trades