# scripts/root_cause.py
import pandas as pd

def infer_root_cause(row):
    causes = []

    if row["packet_loss_pct"] > 2:
        causes.append(("WAN Packet Loss", 0.8))

    if row["latency_ms"] > 200 and row["jitter_ms"] > 50:
        causes.append(("WAN Congestion", 0.85))

    if row["throughput_mbps"] < 20:
        causes.append(("Link Saturation", 0.75))

    if row["ml_anomaly"] == 1 and row["health_score"] < 60:
        causes.append(("Abnormal Network Behavior", 0.7))

    if not causes:
        return "Normal Operation", 0.95

    # pick highest confidence
    causes.sort(key=lambda x: x[1], reverse=True)
    return causes[0]


def run_rca(csv_path):
    df = pd.read_csv(csv_path)

    results = df.apply(
        lambda r: infer_root_cause(r),
        axis=1,
        result_type="expand"
    )

    df["root_cause"] = results[0]
    df["root_cause_confidence"] = results[1]

    df.to_csv(csv_path, index=False)
    print("Root Cause Analysis completed.")


if __name__ == "__main__":
    run_rca("../data/network_metrics.csv")
