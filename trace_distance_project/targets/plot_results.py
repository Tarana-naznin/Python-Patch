import json
import matplotlib.pyplot as plt
import os

# Load results from the JSON file
input_name = input("Enter Project name to plot: ").strip().lower()
file_path = os.path.join("comparison_results", f"{input_name}_comparison_results.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract data
sha_values = [entry["sha"] for entry in data]
ld_values = [entry["LD"] for entry in data]
lcs_values = [entry["LCS"] for entry in data]

# Plot Levenshtein Distance
plt.figure(figsize=(10, 5))
plt.bar(sha_values, ld_values)
plt.xlabel("SHA")
plt.ylabel("Levenshtein Distance")
plt.title(f"Levenshtein Distance for {input_name}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Plot Longest Common Subsequence
plt.figure(figsize=(10, 5))
plt.bar(sha_values, lcs_values)
plt.xlabel("SHA")
plt.ylabel("Longest Common Subsequence")
plt.title(f"LCS for {input_name}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
