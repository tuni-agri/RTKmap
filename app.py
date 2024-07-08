from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/points")
def points():
    # Lue JSON-tiedosto
    with open('points.json') as f:
        points = json.load(f)
    return jsonify(points)

if __name__ == "__main__":
    app.run(debug=True)