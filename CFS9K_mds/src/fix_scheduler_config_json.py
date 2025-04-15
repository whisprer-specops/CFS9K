# Fix: import json and retry writing scheduler_config.json

import json

config = {
    "enabled": True,
    "interval_minutes": 60,
    "wave_count": 1,
    "cards": 50,
    "min_amount": 0.15,
    "max_amount": 4.75,
    "spread_minutes": 45,
    "merchant_count": 5,
    "wallet_count": 3
}

config_path = Path("/mnt/data/CFS9K/backend/utils/scheduler_config.json")
config_path.write_text(json.dumps(config, indent=4))

config_path
Result
PosixPath('/mnt/data/CFS9K/backend/utils/scheduler_config.json')