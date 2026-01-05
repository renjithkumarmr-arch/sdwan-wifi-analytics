# scripts/llm_context.py
import pandas as pd

def build_llm_prompt(row):
    return f"""
You are a Network Operations Copilot.

Incident Summary:
- Device: {row['device']}
- Health Score: {row['health_score']}
- Anomaly Detected: {row['ml_anomaly']}
- Root Cause: {row['root_cause']} (confidence {row['root_cause_confidence']})
- Recommended Action: {row['rl_recommendation']}

Explain the issue clearly and suggest next steps.
"""

def generate_prompts(csv_path):
    df = pd.read_csv(csv_path)
    df["llm_prompt"] = df.apply(build_llm_prompt, axis=1)
    df.to_csv(csv_path, index=False)
    print("LLM prompts generated.")


if __name__ == "__main__":
    generate_prompts("../data/network_metrics.csv")
