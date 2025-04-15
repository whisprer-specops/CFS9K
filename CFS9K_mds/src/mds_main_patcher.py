# Patch backend/main.py with a new FastAPI endpoint to trigger the siphon simulation

simulate_siphon_endpoint = """
from utils.siphon_engine import run_siphon_simulation

@app.post("/simulate_siphon")
def simulate_siphon():
    config = {
        "cards": 50,
        "min_amount": 0.12,
        "max_amount": 4.79,
        "spread_minutes": 30,
        "merchant_count": 5,
        "wallet_count": 3
    }
    log = run_siphon_simulation(config)
    return {"total_attempts": len(log), "successful": sum(1 for x in log if x["success"]), "log": log}
"""

# Write to main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
with open(main_path, "a") as f:
    f.write(simulate_siphon_endpoint)

# Confirm new API route added
main_path
Result
PosixPath('/mnt/data/CFS9K/backend/main.py')