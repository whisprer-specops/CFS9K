# Update monitor.html to include:
# - dynamic trap map image
# - timer countdown since last high-risk event

monitor_html_updated = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>CFS9K Dashboard</title>
  <style>
    body {
      background-color: #121212;
      color: #e0e0e0;
      font-family: 'Courier New', Courier, monospace;
      padding: 20px;
    }
    h1 { color: #ff4081; }
    #log { white-space: pre-line; background: #1e1e1e; padding: 15px; border-radius: 5px; }
    .alert { color: #ff5252; font-weight: bold; }
    .timer { margin-top: 20px; color: #f44336; font-size: 1.2em; }
  </style>
</head>
<body>
  <h1>🔍 CFS9K Monitoring Dashboard</h1>
  <div id="log">Connecting to backend...</div>

  <div class="timer">
    ⏱️ Time since last high-risk activity: <span id="alertTimer">0</span> seconds
  </div>

  <h2>🕷️ Honeypot Trap Map</h2>
  <img id="trapmap" src="http://localhost:8000/trapmap" width="600" />

  <script src="https://cdn.socket.io/4.3.2/socket.io.min.js"></script>
  <script>
    let alertTime = 0;
    const socket = io("http://localhost:8000");
    const log = document.getElementById("log");
    const timerDisplay = document.getElementById("alertTimer");

    setInterval(() => {
      alertTime++;
      timerDisplay.textContent = alertTime;
      document.getElementById("trapmap").src = "http://localhost:8000/trapmap?t=" + new Date().getTime();
    }, 1000);

    socket.on("connect", () => {
      log.textContent = "Connected to backend. Waiting for events...\\n";
    });

    socket.on("suspicious_activity", data => {
      alertTime = 0;
      const msg = `🚨 Suspicious Laundering Detected:
Mixer: ${data.mixer}
Reason: ${data.reason}
Action: ${data.response}
----------------------------------\\n`;
      log.innerText += msg;
    });

    socket.on("normal_activity", data => {
      const msg = `✅ Clean Activity:
Mixer: ${data.mixer}
Hops: ${data.hops.join(" → ")}
----------------------------------\\n`;
      log.innerText += msg;
    });
  </script>
</body>
</html>
"""

# Write updated monitor.html
monitor_html_path = Path("/mnt/data/CFS9K/frontend/monitor.html")
monitor_html_path.write_text(monitor_html_updated)

monitor_html_path
