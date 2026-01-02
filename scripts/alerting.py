import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(BASE_DIR, "data", "network_metrics.csv")

df = pd.read_csv(data_file)

# Ensure 'severity' column exists
if 'severity' not in df.columns:
    print("No 'severity' column found. Run anomaly_detection.py first.")
else:
    high_severity = df[df['severity'] == 'Critical']
    if not high_severity.empty:
        print("Critical anomalies detected:")
        print(high_severity.to_string(index=False))
    else:
        print("No critical anomalies detected.")
