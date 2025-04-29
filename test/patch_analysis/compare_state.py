def test_states(divide_fn):
    a, b = 4, 0
    print("Inputs:", a, b)
    try:
        result = divide_fn(a, b)
        print("Output:", result)
    except Exception as e:
        print("Crashed with:", e)

if __name__ == "__main__":
    import importlib.util

    for label, path in [("buggy", "buggy_version/divide.py"),
                        ("patched", "patched_version/divide.py")]:
        print(f"\n--- {label.upper()} STATE ---")
        spec = importlib.util.spec_from_file_location(label, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        test_states(mod.divide)
