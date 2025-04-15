# Patch heatmap_viz.py to include metadata export with success rate per wave

heatmap_wave_patch = """
def render_siphon_heatmap(log_path="utils/siphon_log.json", output_path="utils/siphon_heatmap.png", wave_id=None):
    with open(log_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['minute'] = df['timestamp'].dt.floor('min')
    df['hour'] = df['timestamp'].dt.hour
    df['minute_of_hour'] = df['timestamp'].dt.minute

    pivot = df.pivot_table(index="hour", columns="minute_of_hour", values="success", aggfunc="count", fill_value=0)

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.5, linecolor="gray", annot=True, fmt="d")
    title = f"🔥 Siphon Heatmap{' - Wave #' + str(wave_id) if wave_id is not None else ''}"
    plt.title(title, fontsize=14)
    plt.xlabel("Minute of Hour")
    plt.ylabel("Hour (UTC)")
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    # metadata
    total = len(df)
    success = df['success'].sum()
    metadata = {
        "wave_id": wave_id,
        "total_attempts": total,
        "successful": int(success),
        "success_rate": round(success / total, 2) if total > 0 else 0.0,
        "log_file": str(log_path),
        "heatmap_file": str(output_path)
    }

    metadata_path = str(output_path).replace(".png", ".json")
    with open(metadata_path, "w") as mf:
        json.dump(metadata, mf, indent=4)

    return output_path
"""

# Append to heatmap_viz.py
heatmap_path = Path("/mnt/data/CFS9K/backend/utils/heatmap_viz.py")
with open(heatmap_path, "a") as f:
    f.write(heatmap_wave_patch)

heatmap_path
Result
PosixPath('/mnt/data/CFS9K/backend/utils/heatmap_viz.py')