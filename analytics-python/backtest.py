import pandas as pd

from engine import BacktestEngine
from strategies.mean import MeanStrategy
from strategies.boll import BollStrategy
from strategies.momentum import MomentumStrategy
import db

from metrics import calculate_metrics

def load_data():

    sql="""

    SELECT
    ts,
    spread,
    zscore,
    ma20,
    ma60,
    std20
    FROM analytics_records
    ORDER BY ts
    """
    conn=db.get_conn()
    df=pd.read_sql(sql,conn)
    conn.close()
    return df


def save_result(trades):
    conn = db.get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
            INSERT INTO backtest_result
            (
                entry_time,
                exit_time,
                entry_spread,
                exit_spread,
                direction,
                pnl,
                fee,
                hold_seconds,
                pnl_after_fee
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = []
            for trade in trades:
                values.append((
                    trade.entry_time,
                    trade.exit_time,
                    trade.entry_spread,
                    trade.exit_spread,
                    trade.direction,
                    trade.pnl,
                    trade.fee,
                    trade.hold_seconds,
                    trade.pnl_after_fee
                ))
            cur.executemany(sql, values)
        conn.commit()
    finally:
        conn.close()

def save_metrics(strategy, result):
    conn = db.get_conn()
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO backtest_metrics
        (
        strategy,
        trade_count,
        win_rate,
        total_pnl,
        avg_pnl,
        profit_factor,
        max_drawdown,
        sharpe,
        avg_hold
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
        strategy,
        result["trade_count"],
        result["win_rate"],
        result["total_pnl"],
        result["avg_pnl"],
        result["profit_factor"],
        result["max_drawdown"],
        result["sharpe"],
        result["avg_hold"]
        ))
    conn.commit()
    conn.close()



if __name__=="__main__":
    df=load_data()
    strategies=[
        MeanStrategy(),
        BollStrategy(),
        MomentumStrategy()
    ]

    for strategy in strategies:
        print("\n====================")
        print(strategy.__class__.__name__)
        engine = BacktestEngine(strategy)
        trades = engine.run(df)
        save_result(trades)
        result = calculate_metrics(trades)
        print(result)
        save_metrics(strategy.__class__.__name__,result)