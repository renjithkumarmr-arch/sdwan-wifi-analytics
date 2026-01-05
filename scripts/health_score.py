# scripts/health_score.py
import pandas as pd

# -----------------------------------------
# Health Score Computation Logic
# -----------------------------------------
def compute_health_score(row):
    """
    Health Score starts at 100 and degrades based on:
    - Latency
    - Packet loss
    - Jitter
    - Throughput
    - ML anomaly flag
    """

    score = 100

    # Latency impact
    if row["latency_ms"] > 100:
        score -= min((row["latency_ms"] - 100) * 0.2, 25)

    # Packet loss impact (very strong)
    score -= min(row["packet_loss_pct"] * 10, 30)

    # Jitter impact
    score -= min(row["jitter_ms"] * 0.5, 20)

    # Throughput degradation
    if row["throughput_mbps"] < 50:
        score -= min((50 - row["throughput_mbps"]) * 0.5, 15)

    # ML anomaly penalty
    if row.get("ml_anomaly", 0) == 1:
        score -= 20

    return max(int(score), 0)

# -----------------------------------------
# Run Health Score Engine
# -----------------------------------------
def run_health_score(csv_path):
    df = pd.read_csv(csv_path)

    # Ensure ml_anomaly exists
    if "ml_anomaly" not in df.columns:
        df["ml_anomaly"] = 0

    df["health_score"] = df.apply(compute_health_score, axis=1)

    # Health band (optional but useful)
    df["health_status"] = pd.cut(
        df["health_score"],
        bins=[-1, 59, 79, 100],
        labels=["Critical", "Degraded", "Healthy"]
    )

    df.to_csv(csv_path, index=False)
    print("Health Score calculated and saved.")

# -----------------------------------------
# Entry point
# -----------------------------------------
if __name__ == "__main__":
    run_health_score("../data/network_metrics.csv")
