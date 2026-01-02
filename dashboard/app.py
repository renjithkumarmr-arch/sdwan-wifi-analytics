import pandas as pd
import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "network_metrics.csv")

# -------------------------------------------------
# Severity colors
# -------------------------------------------------
COLOR_MAP = {
    "Normal": "green",
    "Warning": "orange",
    "Critical": "red"
}

# -------------------------------------------------
# Safe column helper
# -------------------------------------------------
def safe_col(df, col, default):
    if col not in df.columns:
        df[col] = default
    return df

# -------------------------------------------------
# KPI builder
# -------------------------------------------------
def build_kpis(df):
    df = safe_col(df, "health_score", 100)
    df = safe_col(df, "breach_pred", 0)

    critical = (df["health_score"] < 60).sum()
    warning = ((df["health_score"] >= 60) & (df["health_score"] < 80)).sum()
    healthy = (df["health_score"] >= 80).sum()
    predicted = (df["breach_pred"] == 1).sum()

    return critical, warning, healthy, predicted

# -------------------------------------------------
# Metric chart (SLA color + anomaly marker)
# -------------------------------------------------
def metric_chart(df, metric, sev_col, title, y_label):
    df = safe_col(df, sev_col, "Normal")
    df = safe_col(df, "ml_anomaly", 0)

    fig = go.Figure()

    for sev in ["Normal", "Warning", "Critical"]:
        subset = df[df[sev_col] == sev]

        fig.add_trace(
            go.Scatter(
                x=subset["timestamp"],
                y=subset[metric],
                mode="markers",
                name=sev,
                marker=dict(
                    color=COLOR_MAP[sev],
                    size=subset["ml_anomaly"].map(lambda x: 14 if x == 1 else 8),
                    symbol=subset["ml_anomaly"].map(lambda x: "x" if x == 1 else "circle"),
                    line=dict(width=1)
                ),
                hovertemplate=(
                    "Device: %{customdata[0]}<br>"
                    f"{y_label}: %{{y}}<br>"
                    "Severity: " + sev + "<br>"
                    "Anomaly: %{customdata[1]}<br>"
                    "<extra></extra>"
                ),
                customdata=subset[["device", "ml_anomaly"]].values
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=y_label,
        height=330,
        legend_title="Severity"
    )

    return fig

# -------------------------------------------------
# Health score chart
# -------------------------------------------------
def health_chart(df):
    df = safe_col(df, "health_score", 100)
    df = safe_col(df, "breach_probability", 0.0)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["health_score"],
            mode="lines+markers",
            marker=dict(
                color=df["health_score"],
                colorscale="RdYlGn",
                cmin=0,
                cmax=100,
                size=8
            ),
            hovertemplate=(
                "Device: %{customdata[0]}<br>"
                "Health Score: %{y}<br>"
                "SLA Risk (15 min): %{customdata[1]:.2f}"
                "<extra></extra>"
            ),
            customdata=df[["device", "breach_probability"]].values
        )
    )

    fig.update_layout(
        title="Overall Health Score",
        yaxis_title="Health (0–100)",
        height=350
    )

    return fig

# -------------------------------------------------
# Dash App
# -------------------------------------------------
app = Dash(__name__)
app.title = "SD-WAN WiFi Analytics"

app.layout = html.Div(
    style={"padding": "20px"},
    children=[
        html.H1("SD-WAN WiFi Analytics Dashboard"),

        dcc.Interval(id="refresh", interval=5 * 1000, n_intervals=0),

        html.Div(
            style={"display": "flex", "justifyContent": "space-around"},
            children=[
                html.Div(id="kpi-critical"),
                html.Div(id="kpi-warning"),
                html.Div(id="kpi-healthy"),
                html.Div(id="kpi-predicted"),
            ]
        ),

        html.Hr(),

        dcc.Graph(id="health-chart"),
        dcc.Graph(id="latency-chart"),
        dcc.Graph(id="jitter-chart"),
        dcc.Graph(id="packetloss-chart"),
        dcc.Graph(id="throughput-chart"),
    ]
)

# -------------------------------------------------
# Callback
# -------------------------------------------------
@app.callback(
    Output("kpi-critical", "children"),
    Output("kpi-warning", "children"),
    Output("kpi-healthy", "children"),
    Output("kpi-predicted", "children"),
    Output("health-chart", "figure"),
    Output("latency-chart", "figure"),
    Output("jitter-chart", "figure"),
    Output("packetloss-chart", "figure"),
    Output("throughput-chart", "figure"),
    Input("refresh", "n_intervals")
)
def refresh_dashboard(n):
    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    crit, warn, healthy, predicted = build_kpis(df)

    return (
        html.H3(f"🔴 Critical Sites: {crit}"),
        html.H3(f"🟠 Degraded Sites: {warn}"),
        html.H3(f"🟢 Healthy Sites: {healthy}"),
        html.H3(f"⚠ Predicted SLA Breach (15 min): {predicted}"),
        health_chart(df),
        metric_chart(df, "latency_ms", "latency_sev", "Latency (ms)", "Latency (ms)"),
        metric_chart(df, "jitter_ms", "jitter_sev", "Jitter (ms)", "Jitter (ms)"),
        metric_chart(df, "packet_loss_pct", "packet_loss_sev", "Packet Loss (%)", "Packet Loss (%)"),
        metric_chart(df, "throughput_mbps", "throughput_sev", "Throughput (Mbps)", "Throughput (Mbps)")
    )

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
