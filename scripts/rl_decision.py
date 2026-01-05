# scripts/rl_decision.py
import pandas as pd

# --------------------------------------------------
# Decision Policy (Rule-based RL surrogate)
# --------------------------------------------------
def recommend_action(row):
    """
    Returns a safe, human-readable recommendation.
    This simulates an RL policy without automation risk.
    """

    # Severe network condition
    if row["health_score"] < 60:
        if row["packet_loss_pct"] > 2:
            return "Shift critical traffic to Broadband"
        if row["latency_ms"] > 200:
            return "Prefer low-latency path (MPLS/Direct)"
        return "Reduce non-business traffic"

    # Degraded condition
    if 60 <= row["health_score"] < 80:
        if row["ml_anomaly"] == 1:
            return "Monitor closely – anomaly detected"
        return "No immediate action – observe"

    # Healthy network
    return "No action required"

# --------------------------------------------------
# Apply recommendations
# --------------------------------------------------
def run_rl_decision(csv_path):
    df = pd.read_csv(csv_path)

    # Safety checks
    required_cols = [
        "health_score",
        "latency_ms",
        "packet_loss_pct",
        "ml_anomaly"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    df["rl_recommendation"] = df.apply(recommend_action, axis=1)

    df.to_csv(csv_path, index=False)
    print("RL decision recommendations generated.")

# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    run_rl_decision("../data/network_metrics.csv")
