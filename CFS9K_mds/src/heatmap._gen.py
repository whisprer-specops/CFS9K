# Create a heatmap visualizer script: heatmap_viz.py

heatmap_code = """
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
from pathlib import Path

def render_siphon_heatmap(log_path="utils/siphon_log.json", output_path="utils/siphon_heatmap.png"):
    with open(log_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['minute'] = df['timestamp'].dt.floor('min')
    df['hour'] = df['timestamp'].dt.hour
    df['minute_of_hour'] = df['timestamp'].dt.minute

    # Create pivot for heatmap
    pivot = df.pivot_table(index="hour", columns="minute_of_hour", values="success", aggfunc="count", fill_value=0)

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.5, linecolor="gray", annot=True, fmt="d")
    plt.title("🧯 Siphon Attack Timeline Heatmap (Attempts/min)", fontsize=14)
    plt.xlabel("Minute of Hour")
    plt.ylabel("Hour (UTC)")
    plt.tight_layout()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    return output_path
"""

# Write to backend/utils/heatmap_viz.py
heatmap_path = Path("/mnt/data/CFS9K/backend/utils/heatmap_viz.py")
heatmap_path.write_text(heatmap_code)

# Add /siphon_heatmap endpoint to backend
heatmap_endpoint = """
from fastapi.responses import FileResponse
from utils.heatmap_viz import render_siphon_heatmap

@app.get("/siphon_heatmap")
def siphon_heatmap():
    output_path = render_siphon_heatmap()
    return FileResponse(output_path)
"""

# Append to main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
with open(main_path, "a") as f:
    f.write(heatmap_endpoint)

# Confirm updated path
[str(heatmap_path), str(main_path)]
Result
['/mnt/data/CFS9K/backend/utils/heatmap_viz.py',
 '/mnt/data/CFS9K/backend/main.py']