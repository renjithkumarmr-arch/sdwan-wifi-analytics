📊 AI-Native Autonomous NOC (SD-WAN & Wi-Fi Analytics)
🚀 Overview

This project demonstrates an AI-Native Network Operations Center (NOC) that:

Detects anomalies proactively

Calculates network health scores

Predicts SLA breaches

Performs root cause analysis

Recommends corrective actions

Provides LLM-based explanations

Designed for enterprise SD-WAN and Wi-Fi environments with safety and explainability.

🧠 Key Capabilities

✔ Anomaly Detection (Isolation Forest)
✔ Site Health Scoring
✔ SLA Breach Prediction (15–30 min)
✔ Root Cause AI
✔ Reinforcement Learning–style Recommendations
✔ LLM-based NOC Copilot Context
✔ Dash-based Visualization

🏗 Architecture Layers

Telemetry Ingestion

Latency, jitter, packet loss, throughput

Device and site context

AI/ML Intelligence

anomaly_detection.py

health_score.py

root_cause.py

Decision Intelligence

rl_decision.py

Safe, explainable recommendations

Explainability Layer

llm_context.py

Incident summaries for operators

Visualization

Dash dashboard with KPIs & charts

📂 Project Structure
sdwan-wifi-analytics/
│
├── data/
│   └── network_metrics.csv
│
├── scripts/
│   ├── collect_data.py
│   ├── anomaly_detection.py
│   ├── health_score.py
│   ├── root_cause.py
│   ├── rl_decision.py
│   └── llm_context.py
│
├── dashboard/
│   └── app.py
│
├── README.md
└── requirements.txt

▶️ How to Run
pip install -r requirements.txt

python scripts/collect_data.py
python scripts/anomaly_detection.py
python scripts/health_score.py
python scripts/root_cause.py
python scripts/rl_decision.py
python scripts/llm_context.py

python dashboard/app.py


Open browser:

http://127.0.0.1:8050

🧩 Design Philosophy

No blind automation

Explain every AI decision

Enterprise-safe

Vendor neutral

Future-ready for real-time streaming

🎯 Ideal Use Cases

Enterprise NOC modernization

SD-WAN observability

Wi-Fi performance analytics

AI Ops / NetOps transformation

Architecture & principal engineer interviews