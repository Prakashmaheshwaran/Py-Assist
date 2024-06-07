import platform
import psutil
from flask import jsonify

def get_specs():
    cpu_freq = psutil.cpu_freq()
    specs = {
        "CPU": platform.processor(),
        "Memory": f"{psutil.virtual_memory().total / (1024.0 ** 3):.2f} GB",
        "Storage": f"{psutil.disk_usage('/').total / (1024.0 ** 3):.2f} GB",
        "CPU Frequency": f"{cpu_freq.current / 1000:.2f} GHz"
    }
    return jsonify(specs)
