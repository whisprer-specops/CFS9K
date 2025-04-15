# Create a Wave Gallery HTML section with success rate filtering logic

wave_gallery_patch = """
  <div class="event-list">
    <h2>🌊 Wave Heatmap Gallery</h2>
    <label for="minSuccess">Min Success Rate:</label>
    <input type="range" id="minSuccess" min="0" max="1" step="0.01" value="0.5" oninput="updateWaveGallery()">
    <span id="successDisplay">0.50</span>
    <div id="waveGallery"></div>
  </div>

  <script>
    function updateWaveGallery() {
      const threshold = parseFloat(document.getElementById("minSuccess").value);
      document.getElementById("successDisplay").textContent = threshold.toFixed(2);
      fetch("http://localhost:8000/static/wave_summary.json")
        .then(res => res.json())
        .then(waves => {
          const div = document.getElementById("waveGallery");
          div.innerHTML = "";
          waves.filter(w => w.success_rate >= threshold).forEach(wave => {
            const img = document.createElement("img");
            img.src = "http://localhost:8000/" + wave.heatmap_file;
            img.width = 600;
            const caption = document.createElement("div");
            caption.innerHTML = `<b>Wave #${wave.wave_id}</b> – ${wave.success_rate * 100}% success`;
            div.appendChild(caption);
            div.appendChild(img);
          });
        });
    }

    // Initial load
    updateWaveGallery();
  </script>
</body>
</html>
"""

# Patch monitor.html
monitor_html_path = Path("/mnt/data/CFS9K/frontend/monitor.html")
html = monitor_html_path.read_text()
patched_html = html.replace("</body>", wave_gallery_patch)

# Save update
monitor_html_path.write_text(patched_html)

monitor_html_path
Result
PosixPath('/mnt/data/CFS9K/frontend/monitor.html')