# Update tumbler.py to integrate bot radar scores and trigger honeypots for suspicious origins

enhanced_tumbler_with_radar = """
import uuid
import random
import time
from typing import List
from bot_radar import bot_radar

class Wallet:
    def __init__(self, label=None, honeypot=False):
        self.address = str(uuid.uuid4())[:8]
        self.history = []
        self.label = label or "anon"
        self.honeypot = honeypot
        self.tripped = False
        self.suspicion_score = 0

    def log(self, message):
        self.history.append(f"[{time.strftime('%H:%M:%S')}] {message}")

    def trigger_honeypot(self, source_wallet):
        self.tripped = True
        self.log(f"⚠️ HONEYPOT TRIGGERED by {source_wallet.address} ⚠️")
        self.suspicion_score += 10

class Tumbler:
    def __init__(self, initial_threat_level=0):
        self.wallets = {}
        self.transaction_graph = {}
        self.honeypot_probability = 0.2
        self.avoidance_bias = 0.8
        self.initial_threat_level = initial_threat_level

    def create_wallet(self, label=None) -> Wallet:
        is_honeypot = random.random() < self.honeypot_probability
        wallet = Wallet(label=label, honeypot=is_honeypot)
        self.wallets[wallet.address] = wallet
        return wallet

    def pick_safe_wallet(self, wallets: List[Wallet]) -> Wallet:
        sorted_wallets = sorted(wallets, key=lambda w: w.suspicion_score)
        for wallet in sorted_wallets:
            if random.random() < self.avoidance_bias and wallet.suspicion_score > 0:
                continue
            return wallet
        return random.choice(wallets)

    def tumble(self, source_wallet: Wallet, amount: float, depth=3, fanout=3) -> Wallet:
        current_wallet = source_wallet
        current_wallet.log(f"Start smart tumbling {amount:.4f} BTC with threat level {self.initial_threat_level}")

        for i in range(depth):
            next_wallets = [self.create_wallet() for _ in range(fanout)]
            self.transaction_graph[current_wallet.address] = [w.address for w in next_wallets]

            split = amount / fanout
            for w in next_wallets:
                delay = random.uniform(0.2, 1.2)
                time.sleep(delay)
                w.log(f"Received {split:.4f} BTC from {current_wallet.address} after {delay:.2f}s delay")

                if self.initial_threat_level >= 7:
                    w.trigger_honeypot(current_wallet)
                elif w.honeypot:
                    w.trigger_honeypot(current_wallet)

            current_wallet = self.pick_safe_wallet(next_wallets)

        final_delay = random.uniform(0.5, 2.5)
        time.sleep(final_delay)
        current_wallet.log(f"Tumbling complete after final {final_delay:.2f}s delay.")
        return current_wallet

    def get_transaction_graph(self):
        return self.transaction_graph

    def get_wallet_history(self, address: str) -> List[str]:
        return self.wallets[address].history if address in self.wallets else []

    def get_triggered_honeypots(self):
        return {addr: w.history for addr, w in self.wallets.items() if w.honeypot and w.tripped}

def simulate_card_to_crypto_laundering(card_data):
    # Get the latest radar score for the same IP if available
    threat_level = 0
    recent = bot_radar.get_recent()
    card_ip = card_data.get("ip", "unknown")
    for entry in recent:
        if entry["ip"] == card_ip:
            threat_level = entry["score"]
            break

    tumbler = Tumbler(initial_threat_level=threat_level)
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

# Overwrite tumbler.py with radar-integrated version
(backend_dir / "tumbler.py").write_text(enhanced_tumbler_with_radar)

# Confirm complete
backend_dir / "tumbler.py"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/backend/tumbler.py')