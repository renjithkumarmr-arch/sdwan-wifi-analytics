import pandas as pd

def load_data():
    return pd.read_csv("../data/network_metrics.csv")

def severity_color(severity):
    if severity == 'Critical':
        return 'red'
    elif severity == 'Warning':
        return 'orange'
    else:
        return 'green'
