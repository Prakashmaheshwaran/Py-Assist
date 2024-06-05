from flask import Flask, jsonify
import platform
import psutil

app = Flask(__name__)

@app.route('/specs', methods=['GET'])
def get_specs():
    specs = {
        "CPU": platform.processor(),
        "Memory": f"{psutil.virtual_memory().total / (1024.0 **3):.2f} GB",
        "Storage": f"{psutil.disk_usage('/').total / (1024.0 **3):.2f} GB"
    }
    return jsonify(specs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
