import uuid, random

class Wallet:
    def __init__(self):
        self.address = str(uuid.uuid4())[:8]
        self.history = []

class Tumbler:
    def __init__(self):
        self.graph = {}  # transaction graph

    def tumble(self, source_wallet, amount, depth=3, fanout=3):
        current_wallet = source_wallet
        for i in range(depth):
            next_wallets = [Wallet() for _ in range(fanout)]
            self.graph[current_wallet.address] = [w.address for w in next_wallets]

            # Simulate transaction split
            split = amount / fanout
            for w in next_wallets:
                w.history.append(f"Received {split} from {current_wallet.address}")
            current_wallet = random.choice(next_wallets)
        return current_wallet

    def display_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        for src, targets in self.graph.items():
            for dst in targets:
                G.add_edge(src, dst)
        nx.draw_networkx(G, with_labels=True, node_size=700, font_size=8)
        plt.title("Tumbler Transaction Graph")
        plt.show()
