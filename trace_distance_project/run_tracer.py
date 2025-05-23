import sys
execution_trace = []

def trace_function(frame, event, arg):
    if event in ("call", "line", "return"):
        code = frame.f_code
        trace_entry = {
            "event": event,
            "function": code.co_name,
            "line": frame.f_lineno,
            "locals": {k: repr(v) for k, v in frame.f_locals.items()}
        }
        
        # Add global variables (filtered)
        trace_entry["globals"] = {
            k: repr(v) for k, v in frame.f_globals.items()
            if not k.startswith("__") and not callable(v)
        }

        # Add return value if applicable
        if event == "return":
            trace_entry["return"] = repr(arg)
            
        execution_trace.append(trace_entry)
    return trace_function

def run_traced_code(func):
    global execution_trace
    execution_trace = []
    sys.settrace(trace_function)
    try:
        func()
    finally:
        sys.settrace(None)
    return execution_trace

def identify_basic_blocks(trace):
    blocks = []
    current_block = []
    last_line = None

    for entry in trace:
        if entry["event"] != "line":
            continue

        if last_line is not None and entry["line"] != last_line + 1:
            if current_block:
                blocks.append(current_block)
                current_block = []

        current_block.append(entry)
        last_line = entry["line"]

    if current_block:
        blocks.append(current_block)

    return blocks


# File: field_monitor.py
class MonitoredObject:
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        print(f"[Field Read] {name} = {value}")
        return value

    def __setattr__(self, name, value):
        print(f"[Field Write] {name} = {value}")
        super().__setattr__(name, value)


# File: object_tracker.py
allocations = []

class TrackedObject:
    def __init__(self):
        allocations.append(f"Allocated {self.__class__.__name__}")

def get_allocations():
    return allocations
