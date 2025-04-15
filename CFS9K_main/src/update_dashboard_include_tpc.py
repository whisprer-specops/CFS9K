# Update monitor.html to include a cluster graph gallery section

dashboard_update = """
  <div class="event-list">
    <h2>🧠 Threat Cluster Gallery</h2>
    <button onclick="loadClusterGraphs()">Load Cluster Graphs</button>
    <div id="clusterGallery"></div>
  </div>

  <script>
    // Append this to existing script block

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
  </script>
"""

# Inject the cluster gallery section into monitor.html
monitor_html_path = Path("/mnt/data/CFS9K/frontend/monitor.html")
html_content = monitor_html_path.read_text()

# Insert just before </body>
patched_html = html_content.replace("</body>", dashboard_update + "\n</body>")

# Write patched version
monitor_html_path.write_text(patched_html)

monitor_html_path
