# Create a bot_radar module to track and store live visitor scores in memory

bot_radar_py = """
from collections import deque
import time

class BotRadar:
    def __init__(self, max_entries=100):
        self.visitors = deque(maxlen=max_entries)  # keep a rolling list of recent entries

    def record(self, fingerprint, verdict, score):
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "userAgent": fingerprint.get("userAgent", ""),
            "ip": fingerprint.get("ip", "unknown"),
            "verdict": verdict,
            "score": score
        }
        self.visitors.appendleft(entry)

    def get_recent(self):
        return list(self.visitors)

# Singleton instance
bot_radar = BotRadar()
"""

# Save this as bot_radar.py
(backend_dir / "bot_radar.py").write_text(bot_radar_py)

# Patch main.py to update bot radar and serve the live feed
update_main_py = """
from bot_radar import bot_radar

@app.post("/fingerprint")
async def collect_fingerprint(request: Request):
    data = await request.json()
    client_ip = request.client.host if request.client else "unknown"
    data["ip"] = client_ip
    result = log_and_analyze(data)
    bot_radar.record(data, result["verdict"], result["score"])
    return {
        "message": "Fingerprint received",
        "score": result["score"],
        "verdict": result["verdict"],
        "notes": result["notes"]
    }

@app.get("/radar")
async def get_bot_radar():
    return bot_radar.get_recent()
"""

# Append new radar routes to main.py
with open(backend_dir / "main.py", "a") as f:
    f.write(update_main_py)

# Confirm bot radar setup complete
backend_dir / "bot_radar.py"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/backend/bot_radar.py')
