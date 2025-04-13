# Create basic HTML dashboard to visualize bot radar and honeypot activity

dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fraud Hunter Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #f3f3f3; margin: 0; padding: 2rem; }
        h1 { text-align: center; color: #222; }
        .container { max-width: 1000px; margin: auto; background: #fff; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #ffdd57; }
        .clean { background: #d4edda; }
        .suspicious { background: #fff3cd; }
        .likely-bot { background: #f8d7da; }
        .small { font-size: 0.8em; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Fraud Hunter Dashboard</h1>
        <p class="small">Live monitoring of site visitors, bot detection scores, and laundering risk levels.</p>
        <table id="radar-table">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>IP Address</th>
                    <th>User Agent</th>
                    <th>Score</th>
                    <th>Verdict</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <script>
        async function fetchRadar() {
            const res = await fetch("http://localhost:8000/radar");
            const radar = await res.json();
            const tbody = document.querySelector("#radar-table tbody");
            tbody.innerHTML = "";

            radar.forEach(entry => {
                const tr = document.createElement("tr");
                tr.className = entry.verdict.replace(" ", "-");
                tr.innerHTML = `
                    <td>${entry.timestamp}</td>
                    <td>${entry.ip}</td>
                    <td class="small">${entry.userAgent}</td>
                    <td>${entry.score}</td>
                    <td><strong>${entry.verdict.toUpperCase()}</strong></td>
                `;
                tbody.appendChild(tr);
            });
        }

        setInterval(fetchRadar, 3000);
        fetchRadar();
    </script>
</body>
</html>
"""

# Write the dashboard HTML file
(backend_dir.parent / "frontend" / "dashboard.html").write_text(dashboard_html)

# Confirm path to open dashboard
frontend_dir / "dashboard.html"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/frontend/dashboard.html')
