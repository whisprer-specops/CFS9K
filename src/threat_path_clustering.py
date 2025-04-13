# Generate a new Python module to perform clustering based on historical threat paths

cluster_module_code = """
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from pathlib import Path

HISTORY_PATH = Path("utils/high_risk_history.json")
CLUSTER_OUTPUT_PATH = Path("utils/threat_clusters.json")

def extract_path_features(events):
    paths = []
    for event in events:
        hops = event.get("hops", [])
        path = " -> ".join(hops)
        paths.append(path)
    return paths

def cluster_threat_paths(n_clusters=3):
    try:
        with open(HISTORY_PATH, "r") as f:
            events = json.load(f)
    except FileNotFoundError:
        return []

    if not events:
        return []

    paths = extract_path_features(events)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(paths)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    clustered = []
    for idx, event in enumerate(events):
        clustered.append({
            "event_id": idx,
            "mixer": event.get("mixer", "unknown"),
            "path": event.get("hops", []),
            "cluster": int(labels[idx])
        })

    with open(CLUSTER_OUTPUT_PATH, "w") as f:
        json.dump(clustered, f, indent=4)

    return clustered
"""

# Save this as backend/utils/threat_clustering.py
clustering_path = Path("/mnt/data/CFS9K/backend/utils/threat_clustering.py")
clustering_path.write_text(cluster_module_code)

# Add a new endpoint to backend/main.py for clustering
cluster_endpoint = """
from utils.threat_clustering import cluster_threat_paths

@app.get("/cluster")
def run_clustering():
    results = cluster_threat_paths(n_clusters=3)
    return results
"""

# Append the new endpoint to main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
with open(main_path, "a") as f:
    f.write(cluster_endpoint)

# Return file paths for confirmation
[str(clustering_path), str(main_path)]
