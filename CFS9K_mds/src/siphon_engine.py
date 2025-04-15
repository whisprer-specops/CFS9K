# Create the core engine: siphon_engine.py to simulate the microcharge drip attack

siphon_engine_code = """
import json
import random
import time
import string
from datetime import datetime
from pathlib import Path

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_user_agent():
    ualist = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
        "Mozilla/5.0 (Android 11; Mobile; rv:89.0)"
    ]
    return random.choice(ualist)

def simulate_charge(card, merchant, wallet, amount):
    success_rate = 0.95 if card['risk_profile'] == 'low' else 0.85 if card['risk_profile'] == 'medium' else 0.65
    merchant_uptime = merchant['uptime']
    combined_chance = success_rate * merchant_uptime
    success = random.random() < combined_chance
    return success

def run_siphon_simulation(config):
    cards = load_json("utils/cardpool.json")
    merchants = load_json("utils/merchants.json")
    wallets = load_json("utils/wallets.json")

    log = []
    t0 = time.time()
    for idx, card in enumerate(cards[:config["cards"]]):
        jitter = random.uniform(0, config["spread_minutes"] * 60)
        now = datetime.utcnow().isoformat()

        merchant = random.choice(merchants)
        wallet = random.choice(wallets)
        amount = round(random.uniform(config["min_amount"], config["max_amount"]), 2)

        result = simulate_charge(card, merchant, wallet, amount)

        entry = {
            "timestamp": now,
            "cardholder": card["cardholder"],
            "pan_suffix": card["pan"][-4:],
            "amount": amount,
            "merchant": merchant["name"],
            "wallet": wallet["routing_id"],
            "success": result,
            "ip": random_ip(),
            "user_agent": random_user_agent()
        }
        log.append(entry)

    Path("utils/siphon_log.json").write_text(json.dumps(log, indent=4))
    return log

if __name__ == "__main__":
    config = {
        "cards": 50,
        "min_amount": 0.12,
        "max_amount": 4.79,
        "spread_minutes": 30,
        "merchant_count": 5,
        "wallet_count": 3
    }
    result = run_siphon_simulation(config)
    print(json.dumps(result, indent=2))
"""

# Write to utils/siphon_engine.py
engine_path = Path("/mnt/data/CFS9K/backend/utils/siphon_engine.py")
engine_path.write_text(siphon_engine_code)

engine_path
Result
PosixPath('/mnt/data/CFS9K/backend/utils/siphon_engine.py')