import Levenshtein

def longest_common_subsequence(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]

def compute_all_distances(trace1, trace2):
    ld = Levenshtein.distance(trace1, trace2)
    lcs = longest_common_subsequence(trace1, trace2)
    return {
        "levenshtein_distance": ld,
        "longest_common_subsequence": lcs
    }
