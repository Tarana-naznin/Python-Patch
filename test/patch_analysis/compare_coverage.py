import coverage
import importlib.util

def run_coverage(label, path):
    cov = coverage.Coverage(data_file=f".coverage.{label}")
    cov.start()
    
    # Dynamically load and execute the module
    spec = importlib.util.spec_from_file_location(label, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Run sample inputs
    mod.divide(4, 2)
    try:
        mod.divide(4, 0)
    except:
        pass

    cov.stop()
    cov.save()

def combine_and_report():
    cov = coverage.Coverage(data_file=".coverage.combined")
    cov.combine([".coverage.buggy", ".coverage.patched"])
    cov.save()
    cov.load()

    print("\nCoverage Report:")
    cov.report(show_missing=True)
    
    # Create HTML report
    cov.html_report(directory='htmlcov')
    print("\nHTML coverage report created in 'htmlcov/index.html'.")

if __name__ == "__main__":
    run_coverage("buggy", "buggy_version/divide.py")
    run_coverage("patched", "patched_version/divide.py")
    
    combine_and_report()
