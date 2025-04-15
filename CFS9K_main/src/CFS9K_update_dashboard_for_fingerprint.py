# Update dashboard.html with expandable rows showing fingerprint analysis details

expanded_dashboard_html = """<!DOCTYPE html>
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
        .details { display: none; background: #f9f9f9; font-size: 0.85em; color: #444; }
        .details td { padding: 0.5rem 0.75rem; }
        .toggle-btn { cursor: pointer; color: #007bff; text-decoration: underline; }
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
                    <th></th>
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

            radar.forEach((entry, idx) => {
                const tr = document.createElement("tr");
                tr.className = entry.verdict.replace(" ", "-");
                tr.innerHTML = `
                    <td>${entry.timestamp}</td>
                    <td>${entry.ip}</td>
                    <td class="small">${entry.userAgent}</td>
                    <td>${entry.score}</td>
                    <td><strong>${entry.verdict.toUpperCase()}</strong></td>
                    <td><span class="toggle-btn" onclick="toggleDetails(${idx})">View Details</span></td>
                `;

                const details = document.createElement("tr");
                details.className = "details";
                details.id = "details-" + idx;
                details.innerHTML = `
                    <td colspan="6">
                        <pre id="notes-${idx}">Loading...</pre>
                    </td>
                `;

                tbody.appendChild(tr);
                tbody.appendChild(details);

                fetch(`http://localhost:8000/fingerprint-detail/${entry.ip}`)
                    .then(res => res.json())
                    .then(data => {
                        const pre = document.getElementById("notes-" + idx);
                        pre.textContent = data.notes.join("\\n");
                    })
                    .catch(() => {
                        const pre = document.getElementById("notes-" + idx);
                        pre.textContent = "No notes found for this visitor.";
                    });
            });
        }

        function toggleDetails(idx) {
            const row = document.getElementById("details-" + idx);
            row.style.display = (row.style.display === "table-row") ? "none" : "table-row";
        }

        setInterval(fetchRadar, 3000);
        fetchRadar();
    </script>
</body>
</html>
"""

# Save the expanded version to the dashboard.html file
(backend_dir.parent / "frontend" / "dashboard.html").write_text(expanded_dashboard_html)

# Patch main.py to add fingerprint detail route
detail_route_py = """
@app.get("/fingerprint-detail/{ip}")
async def get_fingerprint_detail(ip: str):
    try:
        with open("fingerprints_detailed.log", "r") as f:
            lines = f.readlines()
        # reverse search for last entry matching IP
        for line in reversed(lines):
            if ip in line:
                obj = json.loads(line)
                return {"notes": obj["analysis"]["notes"]}
    except Exception as e:
        return {"notes": [f"No data found: {str(e)}"]}
    return {"notes": ["No analysis found for this IP."]}
"""

with open(backend_dir / "main.py", "a") as f:
    f.write(detail_route_py)

# Confirm new dashboard version
frontend_dir / "dashboard.html"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/frontend/dashboard.html')
