import numpy as np
import pandas as pd


def calculate_metrics(trades):
    if len(trades) == 0:
        return {}
    df = pd.DataFrame(trades)
    # ==========================
    # 基础统计
    # ==========================
    trade_count = len(df)
    total_pnl = df["pnl_after_fee"].sum()
    avg_pnl = df["pnl_after_fee"].mean()
    win_rate = (
        (df["pnl_after_fee"] > 0).sum()
        / trade_count
    )
    avg_hold = df["hold_seconds"].mean()

    # ==========================
    # Profit Factor
    # ==========================
    gross_profit = df[df.pnl_after_fee > 0]["pnl_after_fee"].sum()
    gross_loss = abs(
        df[df.pnl_after_fee < 0]["pnl_after_fee"].sum()
    )
    if gross_loss == 0:
        profit_factor = 999
    else:
        profit_factor = gross_profit / gross_loss

    # ==========================
    # Equity Curve
    # ==========================
    equity = df["pnl_after_fee"].cumsum()
    running_max = equity.cummax()
    drawdown = equity - running_max
    max_drawdown = drawdown.min()

    # ==========================
    # Sharpe Ratio
    # ==========================
    std = df["pnl_after_fee"].std()
    if std == 0 or np.isnan(std):
        sharpe = 0
    else:
        sharpe = (
            df["pnl_after_fee"].mean()
            / std
        ) * np.sqrt(trade_count)
    return {
        "trade_count": int(trade_count),
        "win_rate": float(win_rate),
        "total_pnl": float(total_pnl),
        "avg_pnl": float(avg_pnl),
        "profit_factor": float(profit_factor),
        "max_drawdown": float(max_drawdown),
        "sharpe": float(sharpe),
        "avg_hold": float(avg_hold)
    }