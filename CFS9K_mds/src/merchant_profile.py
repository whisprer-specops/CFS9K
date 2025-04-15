# Create merchant_profile.py to simulate rotating merchant identities

merchant_profile_code = """
import random

MERCHANT_NAMES = [
    "CloudPay", "BillCenter", "Streamify", "PayNode",
    "EverWidget", "ByteSync", "LinkPress", "QuickTxn",
    "SafeWare", "BrightHost"
]

def generate_merchant_pool(n=5):
    selected = random.sample(MERCHANT_NAMES, min(n, len(MERCHANT_NAMES)))
    merchants = []
    for name in selected:
        merchant_id = f"MID-{random.randint(10000, 99999)}"
        uptime = round(random.uniform(0.85, 0.99), 2)  # chance of being 'live'
        merchants.append({
            "merchant_id": merchant_id,
            "name": name,
            "uptime": uptime
        })
    return merchants

if __name__ == "__main__":
    import json
    merchants = generate_merchant_pool(5)
    with open("utils/merchants.json", "w") as f:
        json.dump(merchants, f, indent=4)
"""

# Write to utils/merchant_profile.py
merchant_path = Path("/mnt/data/CFS9K/backend/utils/merchant_profile.py")
merchant_path.write_text(merchant_profile_code)

merchant_path
Result
PosixPath('/mnt/data/CFS9K/backend/utils/merchant_profile.py')