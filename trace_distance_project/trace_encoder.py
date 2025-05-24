def encode_trace(trace):
    token_map = {}
    counter = 0
    encoded = []

    for entry in trace:
        token = f"{entry['event']}_{entry['function']}_{entry['line']}"
        if token not in token_map:
            token_map[token] = str(counter)
            counter += 1
        encoded.append(token_map[token])

    return ''.join(encoded)
