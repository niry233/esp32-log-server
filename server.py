from flask import Flask, request
import os

app = Flask(__name__)
LOG_PATH = "uploaded_log.txt"

@app.route('/upload', methods=['POST'])
def upload():
    new_data = request.get_data(as_text=True)

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w') as f:
            f.write(new_data)
        return "✅ File created with initial content.\n"

    with open(LOG_PATH, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1].strip() if lines else ""

    incoming_lines = new_data.strip().splitlines()
    added = 0
    with open(LOG_PATH, 'a') as f:
        for line in incoming_lines:
            if line.strip() and line.strip() != last_line:
                f.write(line + "\n")
                last_line = line
                added += 1

    return f"✅ {added} new lines appended.\n"
