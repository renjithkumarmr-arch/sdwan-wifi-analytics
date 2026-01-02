import pandas as pd
import numpy as np
import datetime
import os

# Get project root dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(BASE_DIR, "data", "network_metrics.csv")

# Ensure data folder exists
os.makedirs(os.path.dirname(data_file), exist_ok=True)

# Simulate 50 devices
devices = [f"AP_{i}" for i in range(1, 51)]

# Generate data
rows = []
for device in devices:
    rows.append({
        "timestamp": datetime.datetime.now(),
        "device": device,
        "latency_ms": np.random.randint(10, 250),
        "jitter_ms": np.random.randint(1, 60),
        "packet_loss_pct": np.random.uniform(0, 10),
        "throughput_mbps": np.random.randint(10, 100)
    })

df = pd.DataFrame(rows)

# Append to CSV
if os.path.exists(data_file):
    df.to_csv(data_file, mode='a', header=False, index=False)
else:
    df.to_csv(data_file, index=False)

print(f"Data collected successfully: {data_file}")
