import json
import os
from Levenshtein import distance as levenshtein_distance
from Bio.Align import PairwiseAligner
from difflib import SequenceMatcher


def read_code(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def longest_common_subsequence(a, b):
    matcher = SequenceMatcher(None, a, b)
    return sum(block.size for block in matcher.get_matching_blocks())


def smith_waterman_score(a, b):
    aligner = PairwiseAligner()
    aligner.mode = 'local'
    return aligner.score(a,b)


def compare_versions(base_code, other_code):
    ld = levenshtein_distance(base_code, other_code)
    lcs = longest_common_subsequence(base_code, other_code)
    # sw = smith_waterman_score(base_code, other_code)
    return ld, lcs


def process_sha_folder(sha_path, file_name):
    variant_paths = []
    for variant in sorted(os.listdir(sha_path)):
        file_path = os.path.join(sha_path, variant, file_name)
        if os.path.isfile(file_path):
            variant_paths.append((variant, file_path))

    if not variant_paths or len(variant_paths) < 2:
        return []

    ref_variant, ref_path = variant_paths[0]
    ref_code = read_code(ref_path)

    results = []
    for variant, path in variant_paths[1:]:
        code = read_code(path)
        ld, lcs = compare_versions(ref_code, code)
        results.append({
            "sha": os.path.basename(sha_path),
            "REF": ref_variant,
            "compared_variant": variant,
            "LD": ld,
            "LCS": lcs
        })
    return results


def process_all_sha_folders(base_dir, input_name):
    dataset_dir = os.path.join(base_dir, input_name)
    file_name = input_name + ".c"
    all_results = []
    for sha_folder in sorted(os.listdir(dataset_dir)):
        sha_path = os.path.join(dataset_dir, sha_folder)
        if os.path.isdir(sha_path):
            results = process_sha_folder(sha_path, file_name)
            all_results.extend(results)
    return all_results


if __name__ == "__main__":
    input_name = input("Enter Project name : ").strip().lower()

    current_dir = os.getcwd()
    base_dir = os.path.join(current_dir, "IntroClass-master")
    results = process_all_sha_folders(base_dir, input_name)

    output_dir = "comparison_results"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{input_name}_comparison_results.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"\n All comparison results written to: {output_file}")