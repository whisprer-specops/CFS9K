# Create the Python module for the crypto tumbler simulator integrated with the Card Fraud Simulator
tumbler_py = """
import uuid
import random
import time
from typing import List

class Wallet:
    def __init__(self, label=None):
        self.address = str(uuid.uuid4())[:8]
        self.history = []
        self.label = label or "anon"

    def log(self, message):
        self.history.append(f"[{time.strftime('%H:%M:%S')}] {message}")

class Tumbler:
    def __init__(self):
        self.wallets = {}
        self.transaction_graph = {}

    def create_wallet(self, label=None) -> Wallet:
        wallet = Wallet(label)
        self.wallets[wallet.address] = wallet
        return wallet

    def tumble(self, source_wallet: Wallet, amount: float, depth=3, fanout=3) -> Wallet:
        current_wallet = source_wallet
        current_wallet.log(f"Start tumbling {amount} BTC")

        for i in range(depth):
            next_wallets = [self.create_wallet() for _ in range(fanout)]
            self.transaction_graph[current_wallet.address] = [w.address for w in next_wallets]

            split = amount / fanout
            for w in next_wallets:
                w.log(f"Received {split:.4f} BTC from {current_wallet.address}")
            current_wallet = random.choice(next_wallets)

        current_wallet.log("Tumbling complete. Funds ready for withdrawal.")
        return current_wallet

    def get_transaction_graph(self):
        return self.transaction_graph

    def get_wallet_history(self, address: str) -> List[str]:
        return self.wallets[address].history if address in self.wallets else []

# Simulated integration function
def simulate_card_to_crypto_laundering(card_data):
    tumbler = Tumbler()
    dirty_wallet = tumbler.create_wallet(label="dirty_card_wallet")
    dirty_wallet.log(f"Loaded with 1 BTC from stolen card: {card_data['card_number']}")

    clean_wallet = tumbler.tumble(dirty_wallet, 1.0)
    return {
        "clean_wallet_address": clean_wallet.address,
        "clean_wallet_history": clean_wallet.history,
        "graph": tumbler.get_transaction_graph()
    }
"""

# Write to backend folder
(backend_dir / "tumbler.py").write_text(tumbler_py)

# Update main.py to simulate fraud + trigger tumbler
updated_main_py = (backend_dir / "main.py").read_text() + """

from tumbler import simulate_card_to_crypto_laundering

@app.post("/launder")
async def launder_funds(data: CardData):
    laundering_result = simulate_card_to_crypto_laundering(data.dict())
    return {
        "message": "Funds laundered through crypto tumbler.",
        "clean_wallet": laundering_result["clean_wallet_address"],
        "history": laundering_result["clean_wallet_history"],
        "graph": laundering_result["graph"]
    }
"""

# Overwrite main.py with updated content
(backend_dir / "main.py").write_text(updated_main_py)

# Return updated structure path
project_root
Result
PosixPath('/mnt/data/card_fraud_simulator_9000')
