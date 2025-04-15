# CFS9K: Microcharge Drip Simulator (MDS)
A full simulator of automated, randomized microcharge attacks over time for training, research, and behavioral modeling.

## 1. MODULE OVERVIEW
Module	            Path	          Purpose
`cardpool.py`	        `backend/utils`	  Generates fake card data
`merchant_profile.py`	`backend/utils`	  Creates fake merchant IDs with uptime %
`wallet_router.py`	  `backend/utils`	  Simulates wallet endpoints with laundering risk
`siphon_engine.py`	  `backend/utils`	  Core logic to simulate 1 microcharge wave
`heatmap_viz.py`	    `backend/utils`	  Generates heatmap of attempts over time
`wave_engine.py`	    `backend/utils`	  Schedules multiple waves with delays
`autoscheduler.py`	  `backend/utils`	  Automatically runs waves on interval
`monitor.html`	      `frontend/`	      Full dashboard visualizer

## 2. INSTALL REQUIREMENTS
Install required Python packages:

bash
`pip install faker matplotlib seaborn pandas apscheduler fastapi uvicorn`

## 3. GENERATE DATA

bash
`# Generate cards`
`python3 backend/utils/cardpool.py`

`# Generate merchants`
`python3 backend/utils/merchant_profile.py`

`# Generate laundering wallets`
`python3 backend/utils/wallet_router.py`

Files created:
`utils/cardpool.json`
`utils/merchants.json`
`utils/wallets.json`

## 4. RUN SINGLE MICROCHARGE SIMULATION
Run once:

bash
`python3 backend/utils/siphon_engine.py`

Creates:
`utils/siphon_log.json` → All charge attempts
`utils/siphon_heatmap.png` → Visual heatmap of activity

## 5. RUN MULTI-WAVE SIMULATION
Launch multiple waves:

bash
`curl -X POST http://localhost:8000/simulate_waves -H "Content-Type: application/json" -d '{`
`  "wave_count": 4,`
`  "interval_secs": 1800,`
`  "cards": 50,`
`  "min_amount": 0.22,`
`  "max_amount": 4.88,`
`  "spread_minutes": 30,`
`  "merchant_count": 5,`
`  "wallet_count": 3`
`}'`

Generates:
`utils/siphon_log_<wave>.json`
`utils/siphon_heatmap_<wave>.png`
`utils/siphon_heatmap_<wave>.json`
`utils/wave_summary.json`

## 6. RUN AUTOSCHEDULER (No Cron Required)
Edit the file:

`backend/utils/scheduler_config.json`:

json
`{`
`  "enabled": true,`
`  "interval_minutes": 60,`
`  "wave_count": 1,`
`  "cards": 50,`
`  "min_amount": 0.15,`
`  "max_amount": 4.75,`
`  "spread_minutes": 45,`
`  "merchant_count": 5,`
`  "wallet_count": 3`
`}`

Run this to start scheduling:

bash
`python3 backend/utils/autoscheduler.py`

Runs run_wave_series() at the specified interval.

## 7. LAUNCH DASHBOARD
Run FastAPI:

bash
`uvicorn backend.main:app --reload --port 8000`

Open dashboard:

bash
`frontend/monitor.html`

Features:

- Live trapmap
- Replay of suspicious events
- Cluster gallery
- Microcharge heatmap
- Wave gallery w/ success rate filter

## 8. CONFIG RANGE NOTES
Config	          Type	  Suggested Range	Notes
cards	            int	    10–500	More = longer simulation
min_amount	      float	  0.01–0.99	Below bank notification threshold
max_amount	      float	  1.00–4.99	Below chargeback alert level
spread_minutes	  int	    10–120	Time to distribute charges per wave
interval_minutes	int	    10–180	Time between scheduled waves
merchant_count	  int	    1–10	Simulates different merchant fronts
wallet_count	    int	    1–5	Simulates laundering endpoints

## 9. MANUAL COMMANDS INDEX
bash
`# Run a single wave`
`python3 backend/utils/siphon_engine.py`

`# Run multiple waves (HTTP)`
`curl -X POST http://localhost:8000/simulate_waves -d ...`

`# Generate heatmap from a single log`
`python3 -c "from utils.heatmap_viz import render_siphon_heatmap; render_siphon_heatmap()"`

`# Trigger autoscheduler manually`
`python3 backend/utils/autoscheduler.py`