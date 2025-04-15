# Update tumbler.py to support hidden honeypot wallets that log special traps when interacted with

tumbler_with_honeypots = """
import uuid
import random
import time
from typing import List

class Wallet:
    def __init__(self, label=None, honeypot=False):
        self.address = str(uuid.uuid4())[:8]
        self.history = []
        self.label = label or "anon"
        self.honeypot = honeypot
        self.tripped = False

    def log(self, message):
        self.history.append(f"[{time.strftime('%H:%M:%S')}] {message}")

    def trigger_honeypot(self, source_wallet):
        self.tripped = True
        self.log(f"⚠️ HONEYPOT TRIGGERED by {source_wallet.address} ⚠️")

class Tumbler:
    def __init__(self):
        self.wallets = {}
        self.transaction_graph = {}
        self.honeypot_probability = 0.2  # 20% chance any wallet is a hidden honeypot

    def create_wallet(self, label=None) -> Wallet:
        is_honeypot = random.random() < self.honeypot_probability
        wallet = Wallet(label=label, honeypot=is_honeypot)
        self.wallets[wallet.address] = wallet
        return wallet

    def tumble(self, source_wallet: Wallet, amount: float, depth=3, fanout=3) -> Wallet:
        current_wallet = source_wallet
        current_wallet.log(f"Start tumbling {amount:.4f} BTC")

        for i in range(depth):
            next_wallets = [self.create_wallet() for _ in range(fanout)]
            self.transaction_graph[current_wallet.address] = [w.address for w in next_wallets]

            split = amount / fanout
            for w in next_wallets:
                delay = random.uniform(0.2, 1.2)
                time.sleep(delay)
                w.log(f"Received {split:.4f} BTC from {current_wallet.address} after {delay:.2f}s delay")
                if w.honeypot:
                    w.trigger_honeypot(current_wallet)

            current_wallet = random.choice(next_wallets)

        final_delay = random.uniform(0.5, 2.5)
        time.sleep(final_delay)
        current_wallet.log(f"Tumbling complete after final {final_delay:.2f}s delay. Funds ready for withdrawal.")
        return current_wallet

    def get_transaction_graph(self):
        return self.transaction_graph

    def get_wallet_history(self, address: str) -> List[str]:
        return self.wallets[address].history if address in self.wallets else []

    def get_triggered_honeypots(self):
        return {addr: w.history for addr, w in self.wallets.items() if w.honeypot and w.tripped}

# Simulated integration function
def simulate_card_to_crypto_laundering(card_data):
    tumbler = Tumbler()
    dirty_wallet = tumbler.create_wallet(label="dirty_card_wallet")
    dirty_wallet.log(f"Loaded with 1 BTC from stolen card: {card_data['card_number']}")

    clean_wallet = tumbler.tumble(dirty_wallet, 1.0)
    return {
        "clean_wallet_address": clean_wallet.address,
        "clean_wallet_history": clean_wallet.history,
        "graph": tumbler.get_transaction_graph(),
        "triggered_honeypots": tumbler.get_triggered_honeypots()
    }
"""

# Overwrite tumbler.py with honeypot-enabled version
(backend_dir / "tumbler.py").write_text(tumbler_with_honeypots)

# Confirm update
backend_dir / "tumbler.py"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/backend/tumbler.py')
