This project is a SD-WAN & WiFi analytics dashboard built using Python + Dash.

It shows how network data can be:

Visualized

Analyzed

Monitored

Predicted (before SLA breaks)

Think of it as a mini NOC dashboard with intelligence.

2️⃣ What problems it solves

The dashboard helps answer:

Is my network healthy right now?

Which sites are degraded or critical?

Are there early warning signals before SLA breaks?

Which KPIs are causing issues?

3️⃣ Key features explained
📊 Metrics visualization

You see graphs for:

Latency

Jitter

Packet loss

Throughput

Each dot is:

🟢 Green → Normal

🟠 Orange → Warning

🔴 Red → Critical

❌ Anomaly detection (important!)

Some points show ❌.

This means:

ML thinks this point is unusual

BUT it may not yet break SLA

👉 This gives early warning, not noise.

🧠 Health Score

Each timestamp gets a health score (0–100):

80–100 → Healthy

60–79 → Degraded

< 60 → Critical

This combines multiple KPIs into one number.

⏳ SLA breach prediction

The dashboard predicts:

“Is this site likely to break SLA in the next 15 minutes?”

This appears as:

A KPI counter

Risk shown on hover in charts