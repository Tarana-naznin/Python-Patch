import os
import importlib.util
import json
import matplotlib.pyplot as plt
import Levenshtein
from viztracer import VizTracer
from tests.test_runner import run_tests

PATCH_DIR = "patches"
REF_PATH = "reference/median_ref.py"
TRACE_DIR = "traces"
os.makedirs(TRACE_DIR, exist_ok=True)

def run_trace(module_path, func_name, trace_path):
    spec = importlib.util.spec_from_file_location("mod", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tracer = VizTracer(output_file=trace_path)
    tracer.start()
    for args in [(1, 2, 3), (3, 1, 2), (9, 7, 8), (10, 10, 5)]:
        getattr(mod, func_name)(*args)
    tracer.stop()
    tracer.save()

def extract_trace_sequence(trace_path):
    with open(trace_path) as f:
        data = json.load(f)
    return "".join(
        e["funcName"] for e in data.get("traceEvents", []) if "funcName" in e
    )

def evaluate_patch(patch_path, ref_trace):
    patch_name = os.path.basename(patch_path).replace(".py", "")
    patch_trace_path = os.path.join(TRACE_DIR, f"trace_{patch_name}.json")
    run_trace(patch_path, "median", patch_trace_path)
    patch_trace = extract_trace_sequence(patch_trace_path)
    distance = Levenshtein.distance(ref_trace, patch_trace)
    similarity = 1 - distance / max(len(ref_trace), 1)
    pass_percent = run_tests(patch_path)
    return patch_name, distance, similarity, pass_percent

# Run reference trace
ref_trace_path = os.path.join(TRACE_DIR, "trace_ref.json")
run_trace(REF_PATH, "median", ref_trace_path)
ref_trace = extract_trace_sequence(ref_trace_path)

# Evaluate all patches
results = []
for filename in os.listdir(PATCH_DIR):
    if filename.endswith(".py"):
        patch_path = os.path.join(PATCH_DIR, filename)
        patch_name, dist, sim, pass_percent = evaluate_patch(patch_path, ref_trace)
        results.append((patch_name, dist, sim, pass_percent))

# Plot results
patch_names, distances, similarities, pass_rates = zip(*results)

plt.figure(figsize=(10, 5))
plt.scatter(similarities, pass_rates, c='blue', s=100)
for i, name in enumerate(patch_names):
    plt.annotate(name, (similarities[i], pass_rates[i]))

plt.title("Patch Similarity vs. Pass Percentage")
plt.xlabel("Similarity to Reference (Levenshtein-based)")
plt.ylabel("Pass Rate (%)")
plt.grid(True)
plt.show()
