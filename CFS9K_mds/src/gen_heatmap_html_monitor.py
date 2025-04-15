# Recreate monitor.html with all previous functionality plus the heatmap panel

monitor_html_full = """
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
    .event-list { margin-top: 30px; }
    img { border: 2px solid #444; border-radius: 6px; margin-top: 10px; }
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

  <div class="event-list">
    <h2>📜 Fraud Historian Mode™ — Replay Past Events</h2>
    <label for="eventSelect">Select Event ID:</label>
    <select id="eventSelect"></select>
    <button onclick="replayEvent()">Replay</button>
    <img id="replayImage" width="600" />
  </div>

  <div class="event-list">
    <h2>🧠 Threat Cluster Gallery</h2>
    <button onclick="loadClusterGraphs()">Load Cluster Graphs</button>
    <div id="clusterGallery"></div>
  </div>

  <div class="event-list">
    <h2>🔥 Siphon Heatmap Visualizer</h2>
    <button onclick="loadHeatmap()">Generate Heatmap</button>
    <div><img id="siphonHeatmap" width="800" /></div>
  </div>

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
      fetch("http://localhost:8000/history").then(res => res.json()).then(data => {
        const select = document.getElementById("eventSelect");
        select.innerHTML = "";
        data.forEach((item, i) => {
          const option = document.createElement("option");
          option.value = i;
          option.textContent = `#${i} - ${item.timestamp || "unknown time"} - ${item.mixer}`;
          select.appendChild(option);
        });
      });
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

    function replayEvent() {
      const id = document.getElementById("eventSelect").value;
      const img = document.getElementById("replayImage");
      img.src = `http://localhost:8000/eventgraph/${id}?t=${new Date().getTime()}`;
    }

    function loadClusterGraphs() {
      fetch("http://localhost:8000/clustergraphs")
        .then(res => res.json())
        .then(graphs => {
          const gallery = document.getElementById("clusterGallery");
          gallery.innerHTML = "";
          graphs.forEach(path => {
            const img = document.createElement("img");
            img.src = "http://localhost:8000/" + path;
            img.width = 600;
            gallery.appendChild(img);
          });
        });
    }

    function loadHeatmap() {
      fetch("http://localhost:8000/siphon_heatmap")
        .then(() => {
          document.getElementById("siphonHeatmap").src = "http://localhost:8000/siphon_heatmap?t=" + new Date().getTime();
        });
    }
  </script>
</body>
</html>
"""

# Save full HTML
monitor_html_path = Path("/mnt/data/CFS9K/frontend/monitor.html")
monitor_html_path.parent.mkdir(parents=True, exist_ok=True)
monitor_html_path.write_text(monitor_html_full)

monitor_html_path
Result
PosixPath('/mnt/data/CFS9K/frontend/monitor.html')