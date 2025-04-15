
def check_blacklisted_mixer(mixer_name, blocklist_path="mixer_blocklist.json"):
    import json
    with open(blocklist_path, "r") as f:
        data = json.load(f)
    for category in data.values():
        for entry in category:
            if mixer_name.lower() in entry['name'].lower():
                return True, entry
    return False, None

# Example usage:
if __name__ == "__main__":
    mixer = "ChipMixer"
    flagged, info = check_blacklisted_mixer(mixer)
    if flagged:
        print(f"⚠️ {mixer} is blacklisted: {info['status']}")
    else:
        print(f"✅ {mixer} is not in the blocklist.")
