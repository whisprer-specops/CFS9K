# Create a visualizer that draws clustered paths as graphs colored by cluster

cluster_viz_code = """
import matplotlib.pyplot as plt
import networkx as nx
import json
from pathlib import Path

CLUSTER_PATH = Path("utils/threat_clusters.json")
OUTPUT_DIR = Path("utils/cluster_graphs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def render_clusters():
    try:
        with open(CLUSTER_PATH, "r") as f:
            clustered = json.load(f)
    except FileNotFoundError:
        return []

    cluster_colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta']
    cluster_graphs = {}

    for entry in clustered:
        cid = entry["cluster"]
        if cid not in cluster_graphs:
            cluster_graphs[cid] = nx.DiGraph()
        path = ["origin"] + entry.get("path", []) + ["exit"]
        for i in range(len(path) - 1):
            cluster_graphs[cid].add_edge(path[i], path[i + 1])

    image_paths = []
    for cid, G in cluster_graphs.items():
        pos = nx.spring_layout(G, seed=42)
        color = cluster_colors[cid % len(cluster_colors)]

        plt.figure(figsize=(10, 6))
        nx.draw(
            G, pos, with_labels=True, node_color=color, edge_color='gray',
            node_size=1600, font_size=10, font_color='white'
        )
        plt.title(f"Threat Path Cluster #{cid}", fontsize=14)
        plt.tight_layout()

        path = OUTPUT_DIR / f"cluster_{cid}.png"
        plt.savefig(path)
        plt.close()
        image_paths.append(str(path))

    return image_paths
"""

# Write to backend/utils/cluster_viz.py
viz_path = Path("/mnt/data/CFS9K/backend/utils/cluster_viz.py")
viz_path.write_text(cluster_viz_code)

# Add endpoint to main.py to trigger cluster image generation
cluster_img_route = """
from utils.cluster_viz import render_clusters

@app.get("/clustergraphs")
def get_cluster_graphs():
    return render_clusters()
"""

# Append this to main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
with open(main_path, "a") as f:
    f.write(cluster_img_route)

# Confirm paths
[str(viz_path), str(main_path)]
