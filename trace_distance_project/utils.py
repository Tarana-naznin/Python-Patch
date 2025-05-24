import json

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def get_executed_lines(trace):
    return sorted(set(entry["line"] for entry in trace if entry.get("event") == "line"))