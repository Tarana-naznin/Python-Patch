# Entry point to run a target program with tracing
import os
import json
from run_tracer import run_traced_code, identify_basic_blocks, get_allocations
from trace_encoder import encode_trace
from trace_distance import compute_all_distances
from utils import save_json, get_executed_lines
import targets.original_version as original

def trace_and_compare():
    # Trace original
    trace_original = run_traced_code(original.main)
    blocks_original = identify_basic_blocks(trace_original)
    allocations_original = get_allocations()
    encoded_original = encode_trace(trace_original)
    lines_original = get_executed_lines(trace_original)

    # Save original trace once
    save_json(trace_original, "traces/trace_original.json")
    save_json(blocks_original, "traces/basic_blocks_original.json")
    save_json(allocations_original, "traces/allocations_original.json")

    # Check for patch directory
    patch_dir = "targets/patches"
    if not os.path.exists(patch_dir):
        print(f"No patch directory found at {patch_dir}")
        return

    os.makedirs("reports", exist_ok=True)

    for filename in os.listdir(patch_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module_path = f"targets.patches.{module_name}"

            try:
                patched = __import__(module_path, fromlist=["main"])
                trace_patched = run_traced_code(patched.main)
            except Exception as e:
                print(f"Error running {filename}: {e}")
                continue

            # Collect patch-side data
            blocks_patched = identify_basic_blocks(trace_patched)
            allocations_patched = get_allocations()
            encoded_patched = encode_trace(trace_patched)
            lines_patched = get_executed_lines(trace_patched)

            # Compute distances
            scores = compute_all_distances(encoded_original, encoded_patched)
            scores["original_line_count"] = len(lines_original)
            scores["patched_line_count"] = len(lines_patched)
            scores["original_lines_executed"] = lines_original
            scores["patched_lines_executed"] = lines_patched

            # Combine everything into one report
            report_data = {
                "patch_name": module_name,
                "original_trace": trace_original,
                "patch_trace": trace_patched,
                "original_blocks": blocks_original,
                "patch_blocks": blocks_patched,
                "original_allocations": allocations_original,
                "patch_allocations": allocations_patched,
                "distance": {
                    k: v for k, v in scores.items()
                    if k not in ("original_lines_executed", "patched_lines_executed")
                },
                "executed_lines": {
                    "original": lines_original,
                    "patch": lines_patched
                }
            }

            report_path = f"reports/{module_name}_report.json"
            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2)
            print(f"Generated full report for {filename} → {report_path}")

if __name__ == "__main__":
    trace_and_compare()
