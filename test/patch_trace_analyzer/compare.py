import json
import Levenshtein

def extract_events(path):
    with open(path) as f:
        data = json.load(f)
    return "".join(event["funcName"] for event in data["traceEvents"] if "funcName" in event)

if __name__ == "__main__":
    ref = extract_events("traces/trace_ref.json")
    bug1 = extract_events("traces/trace_bug1.json")

    print("Levenshtein Distance (bug1 vs ref):", Levenshtein.distance(bug1, ref))
