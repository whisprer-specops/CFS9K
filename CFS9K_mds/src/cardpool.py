from pathlib import Path

# Rebuild cardpool.py after state reset
cardpool_code = """
import random
import string
from faker import Faker

fake = Faker()

def generate_fake_card():
    # Simple fake PAN (not valid for real usage)
    pan = ''.join(random.choices(string.digits, k=16))
    expiry = f"{random.randint(1,12):02d}/{random.randint(24,29)}"
    cvv = ''.join(random.choices(string.digits, k=3))
    geo = random.choice(["US", "UK", "FR", "DE", "IN", "BR", "CA"])
    risk_profile = random.choice(["low", "medium", "high"])
    holder = fake.name()

    return {
        "cardholder": holder,
        "pan": pan,
        "expiry": expiry,
        "cvv": cvv,
        "geo": geo,
        "risk_profile": risk_profile
    }

def generate_cardpool(n=1000):
    return [generate_fake_card() for _ in range(n)]

if __name__ == "__main__":
    import json
    cards = generate_cardpool(100)
    with open("utils/cardpool.json", "w") as f:
        json.dump(cards, f, indent=4)
"""

# Save to utils/cardpool.py
utils_path = Path("/mnt/data/CFS9K/backend/utils")
utils_path.mkdir(parents=True, exist_ok=True)
cardpool_path = utils_path / "cardpool.py"
cardpool_path.write_text(cardpool_code)

cardpool_path