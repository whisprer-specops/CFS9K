# Create wave_engine.py for running repeated scheduled simulation waves

wave_engine_code = """
import time
import json
from utils.siphon_engine import run_siphon_simulation
from utils.heatmap_viz import render_siphon_heatmap
from pathlib import Path

def run_wave_series(config):
    wave_count = config.get("wave_count", 3)
    interval_secs = config.get("interval_secs", 1800)

    all_metadata = []

    for wave_id in range(wave_count):
        print(f"Running wave {wave_id + 1}/{wave_count}...")

        wave_config = {
            "cards": config.get("cards", 50),
            "min_amount": config.get("min_amount", 0.12),
            "max_amount": config.get("max_amount", 4.79),
            "spread_minutes": config.get("spread_minutes", 30),
            "merchant_count": config.get("merchant_count", 5),
            "wallet_count": config.get("wallet_count", 3)
        }

        log = run_siphon_simulation(wave_config)
        log_file = f"utils/siphon_log_{wave_id}.json"
        with open(log_file, "w") as f:
            json.dump(log, f, indent=4)

        heatmap_path = f"utils/siphon_heatmap_{wave_id}.png"
        render_siphon_heatmap(log_path=log_file, output_path=heatmap_path, wave_id=wave_id)

        meta_file = heatmap_path.replace(".png", ".json")
        with open(meta_file, "r") as mf:
            metadata = json.load(mf)
            all_metadata.append(metadata)

        if wave_id < wave_count - 1:
            time.sleep(interval_secs)

    # Save combined metadata summary
    Path("utils").mkdir(parents=True, exist_ok=True)
    with open("utils/wave_summary.json", "w") as f:
        json.dump(all_metadata, f, indent=4)

    return all_metadata
"""

# Save wave_engine.py to utils
wave_engine_path = Path("/mnt/data/CFS9K/backend/utils/wave_engine.py")
wave_engine_path.write_text(wave_engine_code)

# Add /simulate_waves endpoint to main.py
simulate_waves_endpoint = """
from utils.wave_engine import run_wave_series

@app.post("/simulate_waves")
def simulate_waves(cfg: dict):
    return run_wave_series(cfg)
"""

# Append to main.py
main_path = Path("/mnt/data/CFS9K/backend/main.py")
with open(main_path, "a") as f:
    f.write(simulate_waves_endpoint)

[str(wave_engine_path), str(main_path)]
Result
['/mnt/data/CFS9K/backend/utils/wave_engine.py',
 '/mnt/data/CFS9K/backend/main.py']