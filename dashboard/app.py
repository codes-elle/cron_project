import sys
import os
# Add the project root to the Python path so that local modules are found.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, render_template
from stats import get_stats

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/stats")
def stats():
    # This returns the current stats as a JSON object.
    return jsonify(get_stats())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
