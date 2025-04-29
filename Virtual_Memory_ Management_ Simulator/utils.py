# utils.py

def calculate_utilization(frames):
    used = sum(1 for f in frames if f is not None)
    return (used / len(frames)) * 100
