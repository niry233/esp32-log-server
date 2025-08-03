from flask import Flask, request
import os

app = Flask(__name__)
LOG_FILE = "log.txt"

@app.route('/upload', methods=['POST'])
def upload():
    data = request.data.decode('utf-8')
    if not data.strip():
        return "Empty data", 400

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write(data + "\n")
    else:
        with open(LOG_FILE, "r+") as f:
            lines = f.readlines()
            if not lines or lines[-1].strip() != data.strip():
                f.write(data + "\n")

    return "OK", 200

@app.route('/log.txt')
def get_log():
    if not os.path.exists(LOG_FILE):
        return "No log yet", 404
    with open(LOG_FILE, "r") as f:
        return f.read(), 200
