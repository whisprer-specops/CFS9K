# Create cloaked JavaScript for fingerprinting + bot detection
fingerprint_js = """
(function () {
    const fp = {
        timestamp: Date.now(),
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screen: {
            width: screen.width,
            height: screen.height,
            colorDepth: screen.colorDepth,
            pixelRatio: window.devicePixelRatio
        },
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        plugins: Array.from(navigator.plugins, p => p.name),
        canvasFingerprint: null,
        webglVendor: null,
        botSignals: []
    };

    // Detect headless/bot environments
    if (navigator.webdriver) fp.botSignals.push("webdriver");
    if (!navigator.plugins.length) fp.botSignals.push("no_plugins");
    if (!navigator.languages || navigator.languages.length === 0) fp.botSignals.push("no_languages");

    // Canvas fingerprinting
    try {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        ctx.textBaseline = "top";
        ctx.font = "14px 'Arial'";
        ctx.fillStyle = "#f60";
        ctx.fillText("CloakedCanvasCheck123", 2, 2);
        fp.canvasFingerprint = canvas.toDataURL();
    } catch (err) {
        fp.canvasFingerprint = "blocked";
        fp.botSignals.push("canvas_blocked");
    }

    // WebGL vendor detection
    try {
        const canvas = document.createElement("canvas");
        const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
        const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
        if (debugInfo) {
            fp.webglVendor = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
        }
    } catch (err) {
        fp.webglVendor = "blocked";
        fp.botSignals.push("webgl_blocked");
    }

    // Send fingerprint to backend
    fetch("http://localhost:8000/fingerprint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(fp)
    });
})();
"""

# Write the script to a new file
(backend_dir.parent / "frontend" / "fingerprint.js").write_text(fingerprint_js)

# Add route to backend to log fingerprint data
fingerprint_route = """
from fastapi import Request

@app.post("/fingerprint")
async def collect_fingerprint(request: Request):
    data = await request.json()
    with open("fingerprints.log", "a") as log:
        log.write(f"\\n--- Fingerprint Received ---\\n{data}\\n")
    return {"message": "Fingerprint logged"}
"""

# Append route to main.py
with open(backend_dir / "main.py", "a") as f:
    f.write(fingerprint_route)

# Inject fingerprint script into honeyshoppe.html
honeyshoppe_path = backend_dir.parent / "frontend" / "honeyshoppe.html"
html = honeyshoppe_path.read_text()
injected = html.replace("</body>", '<script src="fingerprint.js"></script>\n</body>')
honeyshoppe_path.write_text(injected)

# Confirm success
honeyshoppe_path
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/frontend/honeyshoppe.html')
