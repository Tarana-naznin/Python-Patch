import sys

def test_divide(mod):
    print(f"\n--- Testing {mod.__name__} ---")
    print("divide(4, 2) =", mod.divide(4, 2))
    try:
        print("divide(4, 0) =", mod.divide(4, 0))
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    import importlib.util

    for label, path in [("buggy", "buggy_version/divide.py"),
                        ("patched", "patched_version/divide.py")]:
        spec = importlib.util.spec_from_file_location(label, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        test_divide(mod)
