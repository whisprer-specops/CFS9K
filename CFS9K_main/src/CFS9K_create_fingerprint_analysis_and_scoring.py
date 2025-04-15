# Create fingerprint analysis and scoring system
fingerprint_analysis_py = """
import json

def analyze_fingerprint(fp):
    score = 0
    notes = []

    # Bot signal analysis
    if "webdriver" in fp.get("botSignals", []):
        score += 5
        notes.append("Headless browser detected (webdriver)")
    if "no_plugins" in fp.get("botSignals", []):
        score += 2
        notes.append("No browser plugins detected")
    if "no_languages" in fp.get("botSignals", []):
        score += 2
        notes.append("No languages reported by browser")
    if "canvas_blocked" in fp.get("botSignals", []):
        score += 3
        notes.append("Canvas fingerprinting blocked")
    if "webgl_blocked" in fp.get("botSignals", []):
        score += 3
        notes.append("WebGL blocked")

    # User agent red flags
    ua = fp.get("userAgent", "").lower()
    if "headless" in ua or "phantom" in ua:
        score += 4
        notes.append("Suspicious user-agent (headless/phantom)")

    if score == 0:
        notes.append("No strong indicators of automation detected.")

    return {
        "score": score,
        "verdict": "likely bot" if score >= 7 else "suspicious" if score >= 4 else "clean",
        "notes": notes
    }

def log_and_analyze(fp):
    result = analyze_fingerprint(fp)
    entry = {
        "fingerprint": fp,
        "analysis": result
    }
    with open("fingerprints_detailed.log", "a") as log:
        log.write(json.dumps(entry, indent=2) + "\\n")
    return result
"""

# Write to new file
(backend_dir / "fingerprint_analysis.py").write_text(fingerprint_analysis_py)

# Patch main.py to use analysis logic on /fingerprint POSTs
patch_fp_handler = """
from fingerprint_analysis import log_and_analyze

@app.post("/fingerprint")
async def collect_fingerprint(request: Request):
    data = await request.json()
    result = log_and_analyze(data)
    return {
        "message": "Fingerprint received",
        "score": result["score"],
        "verdict": result["verdict"],
        "notes": result["notes"]
    }
"""

# Replace previous fingerprint route in main.py
main_path = backend_dir / "main.py"
main_code = main_path.read_text()

# Remove old raw log-based fingerprint route
main_code = main_code.rsplit("@app.post(\"/fingerprint\")", 1)[0]

# Append new analysis-based route
main_code += patch_fp_handler
main_path.write_text(main_code)

# Confirm update
backend_dir / "fingerprint_analysis.py"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/backend/fingerprint_analysis.py')
