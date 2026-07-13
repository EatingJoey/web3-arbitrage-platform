# visualizer.py
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_candles(df, exchange, symbol):
    # df: pandas DataFrame filtered for single exchange+symbol, must contain timestamp, open, high, low, close
    df = df.sort_values("timestamp")

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
    )

    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=f"{exchange} {symbol}"
        ),
        row=1,
        col=1
    )

    colors = [
    'green' if c >= o else 'red'
    for c, o in zip(df['close'], df['open'])]

    fig.add_trace(
        go.Bar(
            x=df['timestamp'],
            y=df['volume'],
            name="Volume",
            marker_color=colors
        ),
        row=2,
        col=1
    )

    fig.update_layout(
        title=f"{exchange} {symbol}",
        xaxis_rangeslider_visible=False
    )

    # fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
    #                                      open=df['open'],
    #                                      high=df['high'],
    #                                      low=df['low'],
    #                                      close=df['close'],
    #                                      name=f"{exchange} {symbol}")])
    # fig.update_layout(title=f"Candlestick {exchange} {symbol}", xaxis_title="time", yaxis_title=symbol.split('/')[0])
    fig.show()

def plot_close_compare(df, symbol):
    # 比较不同交易所同一symbol的收盘价
    import pandas as pd
    pivot = df[df['symbol']==symbol].pivot_table(index='timestamp', columns='exchange', values='close')
    pivot = pivot.sort_index()
    fig = go.Figure()
    for col in pivot.columns:
        fig.add_trace(go.Scatter(x=pivot.index, y=pivot[col], mode='lines', name=col))
    fig.update_layout(title=f"Close Price Compare: {symbol}", xaxis_title="time", yaxis_title=symbol.split('/')[0])
    fig.show()