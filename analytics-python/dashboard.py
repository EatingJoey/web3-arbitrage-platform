from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import db
import pymysql
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__)


app.layout = html.Div(
    [
        html.H2("WBTC Arbitrage Dashboard"),
        html.Div(
            [
                html.Div(id="spread-card", className="card"),
                html.Div(id="zscore-card", className="card"),
                html.Div(id="std-card", className="card"),
                html.Div(id="update-card", className="card"),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-around",
                "marginBottom": "20px"
            }
        ),
        dcc.Dropdown(
            id="strategy-select",
            options=[
                {"label":"Mean Reversion","value":"MeanStrategy"},
                {"label":"Bollinger","value":"BollStrategy"},
                {"label":"Momentum","value":"MomentumStrategy"},
            ],
            value="MeanStrategy",
            clearable=False,
            style={
                "width":"300px",
                "marginBottom":"20px"
            }),

        html.Div(id="metrics-card"),
        dcc.Graph(id="price-graph"),
        dcc.Graph(id="spread-graph"),
        dcc.Graph(id="zscore-graph"),
        dcc.Graph(id="volatility-graph"),
        dcc.Interval(id="interval", interval=10000, n_intervals=0),  # 10秒刷新
    ]
)


@app.callback(
    [
        Output("price-graph", "figure"),
        Output("spread-graph", "figure"),
        Output("zscore-graph", "figure"),
        Output("volatility-graph", "figure"),
        Output("spread-card","children"),
        Output("zscore-card","children"),
        Output("std-card","children"),
        Output("update-card","children"),
        Output("metrics-card","children")
    ],
    Input("interval", "n_intervals"),
    Input("strategy-select","value")
)
def update_graph(n, strategy):

    conn = db.get_conn()

    # ---------------- Price ----------------
    sql = """
    SELECT
        ts,
        dex_price,
        cex_price
    FROM spread_records
    ORDER BY ts DESC
    LIMIT 5000
    """

    df_price = pd.read_sql(sql, conn)
    df_price = df_price.sort_values("ts")

    df_price["time"] = (
        pd.to_datetime(df_price["ts"], unit="s", utc=True)
        .dt.tz_convert("Asia/Shanghai")
    )

    # ---------------- Analytics ----------------
    sql = """
    SELECT
        ts,
        spread,
        ma20,
        ma60,
        std20,
        zscore
    FROM analytics_records
    ORDER BY ts DESC
    LIMIT 5000
    """

    df = pd.read_sql(sql, conn)
    conn.close()

    df = df.sort_values("ts")

    df["time"] = (
        pd.to_datetime(df["ts"], unit="s", utc=True)
        .dt.tz_convert("Asia/Shanghai")
    )

    conn2=db.get_conn()
    sql="""
        SELECT *
        FROM backtest_metrics
        WHERE strategy=%s
        ORDER BY id DESC
        LIMIT 1
        """
    metric=pd.read_sql(sql,conn2,params=[strategy])
    conn2.close()
    if metric.empty:
        metric_card=html.Div("No Backtest")
    else:
        m=metric.iloc[0]
        metric_card=html.Div([
            html.Div([
                html.H5("Trades"),
                html.H3(int(m.trade_count))
            ], className="metric"),

            html.Div([
                html.H5("Win Rate"),
                html.H3(f"{m.win_rate:.2f}%")
            ], className="metric"),

            html.Div([
                html.H5("Sharpe"),
                html.H3(f"{m.sharpe:.2f}")
            ], className="metric"),

            html.Div([
                html.H5("Max DD"),
                html.H3(f"{m.max_drawdown:.2f}")
            ], className="metric"),

            html.Div([
                html.H5("Profit"),
                html.H3(f"{m.total_pnl:.2f}")
            ], className="metric"),

            html.Div([
                html.H5("Avg PnL"),
                html.H3(f"{m.avg_pnl:.2f}")
            ], className="metric"),

            html.Div([
                html.H5("PF"),
                html.H3(f"{m.profit_factor:.2f}")
            ], className="metric"),

            html.Div([
                html.H5("Hold"),
                html.H3(f"{m.avg_hold:.0f}s")
            ], className="metric"),

        ],
        style={
            "display":"grid",
            "gridTemplateColumns":"repeat(4,1fr)",
            "gap":"20px"
        })

    # ======================================================
    # Price
    # ======================================================

    fig_price = go.Figure()

    fig_price.add_trace(
        go.Scatter(
            x=df_price["time"],
            y=df_price["dex_price"],
            name="DEX",
        )
    )

    fig_price.add_trace(
        go.Scatter(
            x=df_price["time"],
            y=df_price["cex_price"],
            name="CEX",
        )
    )

    fig_price.update_layout(
        title="Price",
        height=400,
    )

    # ======================================================
    # Spread + MA
    # ======================================================

    fig_spread = go.Figure()

    fig_spread.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["spread"],
            name="Spread",
            line=dict(width=2),
        )
    )

    fig_spread.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["ma20"],
            name="MA20",
            line=dict(dash="dash"),
        )
    )

    fig_spread.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["ma60"],
            name="MA60",
            line=dict(dash="dot"),
        )
    )

    fig_spread.add_hline(y=0)

    fig_spread.add_hline(
        y=0.5,
        line_dash="dot",
    )

    fig_spread.add_hline(
        y=-0.5,
        line_dash="dot",
    )

    fig_spread.update_layout(
        title="Spread / MA20 / MA60",
        height=450,
    )

    # ======================================================
    # Z-score
    # ======================================================

    fig_z = go.Figure()

    fig_z.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["zscore"],
            name="Z-score",
        )
    )

    fig_z.add_hline(y=2, line_dash="dot")
    fig_z.add_hline(y=-2, line_dash="dot")
    fig_z.add_hline(y=0)

    fig_z.update_layout(
        title="Z-score",
        height=350,
    )

    # ======================================================
    # Volatility
    # ======================================================

    fig_std = go.Figure()

    fig_std.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["std20"],
            name="STD20",
        )
    )

    fig_std.update_layout(
        title="Rolling Volatility (STD20)",
        height=350,
    )
    
    latest = df.iloc[-1]
    zscore = latest["zscore"]
    
    
    zscore = latest["zscore"]

    if zscore >= 2:
        z_color = "#ff4d4f"      # 红
    elif zscore <= -2:
        z_color = "#52c41a"      # 绿
    else:
        z_color = "#888888"      # 灰

    spread_card = html.Div(
    [
        html.H4("Spread"),
        html.H2(f"{latest['spread']:.2f}%")
    ])
    zscore_card = html.Div(
    [
        html.H4("Z-score"),
        html.H2(f"{zscore:.2f}")
    ],
    style={
        "backgroundColor": z_color,
        "padding": "10px",
        "borderRadius": "10px",
        "textAlign": "center",
        "color":"white"
    })
    std_card = html.Div(
    [
        html.H4("STD20"),
        html.H2(f"{latest['std20']:.2f}")
    ])
    update_card = html.Div(
    [
        html.H4("Last Update"),
        html.H2(
            latest["time"].strftime("%H:%M:%S")
        )
    ])
    
    return (
        fig_price,
        fig_spread,
        fig_z,
        fig_std,
        spread_card,
        zscore_card,
        std_card,
        update_card,
        metric_card
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False,
    )