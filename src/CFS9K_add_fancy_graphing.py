import matplotlib.pyplot as plt
import networkx as nx

# Create a script to visualize the laundering graph with honeypots and clean wallet
visualizer_py = """
import matplotlib.pyplot as plt
import networkx as nx
from fastapi.responses import FileResponse
import os

def visualize_laundering_graph(graph_data: dict, clean_wallet: str, honeypots: dict, output_file: str = "graph.png"):
    G = nx.DiGraph()

    # Add edges
    for src, dst_list in graph_data.items():
        for dst in dst_list:
            G.add_edge(src, dst)

    # Set node colors
    node_colors = []
    for node in G.nodes:
        if node == clean_wallet:
            node_colors.append("green")
        elif node in honeypots:
            node_colors.append("red")
        else:
            node_colors.append("gray")

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # Layout for consistent positioning
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="black", node_size=800, font_size=8)
    nx.draw_networkx_labels(G, pos)

    plt.title("Laundering Graph with Honeypots & Clean Exit")
    plt.savefig(output_file)
    plt.close()

    return output_file
"""

# Create visualizer.py file in backend
(backend_dir / "visualizer.py").write_text(visualizer_py)

# Add FastAPI route to generate and serve graph
with open(backend_dir / "main.py", "a") as f:
    f.write("""

from fastapi.responses import FileResponse
from visualizer import visualize_laundering_graph

@app.post("/visualize")
async def visualize(data: CardData):
    result = simulate_card_to_crypto_laundering(data.dict())
    output_file = "graph.png"
    visualize_laundering_graph(
        graph_data=result["graph"],
        clean_wallet=result["clean_wallet_address"],
        honeypots=result["triggered_honeypots"],
        output_file=output_file
    )
    return FileResponse(output_file, media_type="image/png")
""")

# Return the updated backend structure
backend_dir
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/backend')
