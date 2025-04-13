# Write a function to generate the trap map image dynamically for live updates

live_update_code = """
import matplotlib.pyplot as plt
import networkx as nx
import random
from pathlib import Path

def generate_trap_map_image(output_path="utils/honeypot_trap_map.png"):
    G = nx.Graph()
    wallets = [f"wallet_{i}" for i in range(1, 11)]
    traps = random.sample(wallets, 3)
    scores = {w: random.randint(0, 100) for w in wallets}

    for w in wallets:
        is_trap = w in traps
        G.add_node(w, trap=is_trap, score=scores[w])

    edges = [(random.choice(wallets), random.choice(wallets)) for _ in range(15)]
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)
    colors = ['red' if G.nodes[n]['trap'] else 'green' for n in G.nodes]
    sizes = [300 + G.nodes[n]['score'] * 2 for n in G.nodes]
    labels = {n: f"{n}\\nTS:{G.nodes[n]['score']}" for n in G.nodes}

    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, with_labels=True, labels=labels,
        node_color=colors, node_size=sizes,
        font_size=9, font_color='white', edge_color='gray'
    )
    plt.title("Honeypot Trap Map with Threat Scores", fontsize=14)
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
"""

# Write this module into backend/utils
utils_path = Path("/mnt/data/CFS9K/backend/utils")
utils_path.mkdir(parents=True, exist_ok=True)

with open(utils_path / "trapmap.py", "w") as f:
    f.write(live_update_code)

# Add FastAPI route for updating the image
main_patch = """
from fastapi.responses import FileResponse
from utils.trapmap import generate_trap_map_image

@app.get("/trapmap")
async def trapmap():
    path = "utils/honeypot_trap_map.png"
    generate_trap_map_image(path)
    return FileResponse(path)
"""

# Append patch to existing main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
with open(main_path, "a") as f:
    f.write(main_patch)

# Confirm final path to updated backend and image generator
[str(main_path), str(utils_path / "trapmap.py")]
