import importlib.util
from .test_cases import test_inputs

def run_tests(module_path, func_name="median"):
    """Run tests on a given module. Return pass percentage."""
    spec = importlib.util.spec_from_file_location("mod", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    total = len(test_inputs)
    passed = 0
    for a, b, c, expected in test_inputs:
        try:
            result = getattr(mod, func_name)(a, b, c)
            if result == expected:
                passed += 1
        except Exception:
            continue
    return (passed / total) * 100
