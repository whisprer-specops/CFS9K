# Create backend/utils/history.py to track high-risk laundering events

history_tracker_code = """
import json
from datetime import datetime
from pathlib import Path

HISTORY_PATH = Path("utils/high_risk_history.json")

def log_high_risk_event(event):
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    event['timestamp'] = datetime.utcnow().isoformat()
    history.append(event)

    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)

def get_event_by_id(event_id):
    try:
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)
        return history[event_id]
    except (FileNotFoundError, IndexError):
        return None
"""

# Write this to backend/utils/history.py
utils_path = Path("/mnt/data/CFS9K/backend/utils")
utils_path.mkdir(parents=True, exist_ok=True)

history_file_path = utils_path / "history.py"
history_file_path.write_text(history_tracker_code)

# Append import and call to log_high_risk_event in main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
patch_lines = """
from utils.history import log_high_risk_event, get_event_by_id

@app.get("/eventgraph/{event_id}")
def render_event_graph(event_id: int):
    event = get_event_by_id(event_id)
    if not event:
        return {"error": "Event not found."}

    import matplotlib.pyplot as plt
    import networkx as nx
    import random

    G = nx.DiGraph()
    mixer = event.get("mixer", "unknown_mixer")
    hops = ["origin"] + event.get("hops", ["wallet1", "wallet2", "clean_wallet"]) + ["exit"]
    for i in range(len(hops) - 1):
        G.add_edge(hops[i], hops[i + 1], timestamp=f"T{i}")

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='orange', edge_color='gray',
            node_size=1500, font_size=10, font_color='white')
    edge_labels = nx.get_edge_attributes(G, 'timestamp')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(f"🧠 Event Replay: {mixer}", fontsize=14)
    plt.tight_layout()

    output_path = f"utils/event_{event_id}.png"
    plt.savefig(output_path)
    plt.close()

    from fastapi.responses import FileResponse
    return FileResponse(output_path)
"""

# Append to main.py
with open(main_path, "a") as f:
    f.write(patch_lines)

# Confirm all core paths
[str(history_file_path), str(main_path)]
