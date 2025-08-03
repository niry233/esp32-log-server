from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "sensor_data.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            tvoc INTEGER,
            mq135 INTEGER,
            temperature REAL
        )''')

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    required_fields = ["timestamp", "tvoc", "mq135", "temperature"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing data fields"}), 400

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("""
                INSERT INTO sensor_data (timestamp, tvoc, mq135, temperature)
                VALUES (?, ?, ?, ?)
            """, (data["timestamp"], data["tvoc"], data["mq135"], data["temperature"]))
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data", methods=["GET"])
def get_all_data():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 100").fetchall()
    return jsonify([
        {"id": row[0], "timestamp": row[1], "tvoc": row[2], "mq135": row[3], "temperature": row[4]}
        for row in rows
    ])

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
