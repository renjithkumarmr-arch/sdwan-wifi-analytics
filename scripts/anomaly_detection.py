import pandas as pd
import os
from sklearn.ensemble import IsolationForest

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "network_metrics.csv")

df = pd.read_csv(DATA_FILE)

# -------------------------------------------------
# ML Features
# -------------------------------------------------
features = [
    "latency_ms",
    "jitter_ms",
    "packet_loss_pct",
    "throughput_mbps"
]

X = df[features]

# -------------------------------------------------
# Isolation Forest
# -------------------------------------------------
model = IsolationForest(
    n_estimators=150,
    contamination=0.15,   # 5% anomalies
    random_state=42
)

df["ml_score"] = model.fit_predict(X)
df["ml_anomaly"] = df["ml_score"].apply(lambda x: 1 if x == -1 else 0)

df.to_csv(DATA_FILE, index=False)

print("ML anomaly detection completed.")
print(df[["ml_anomaly"]].value_counts())
# --------------------------------------------------
# Behavioral anomaly (sudden change)
# --------------------------------------------------
df["latency_delta"] = df.groupby("device")["latency_ms"].diff().abs()
df["jitter_delta"] = df.groupby("device")["jitter_ms"].diff().abs()

df["behavioral_anomaly"] = (
    (df["latency_delta"] > 30) |
    (df["jitter_delta"] > 15)
).astype(int)

# Combine anomalies
df["ml_anomaly"] = (
    (df["ml_anomaly"] == 1) |
    (df["behavioral_anomaly"] == 1)
).astype(int)