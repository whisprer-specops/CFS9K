@app.get("/eventgraph/{event_id}")
def render_event(event_id: int):
    # Load saved high_risk_history.json
    # Use event['mixer'] and simulated hops to render a single-path graph
