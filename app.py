from flask import Flask, request, jsonify
from pybloom_live import BloomFilter
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# Configuration: Capacity for 100k users with 0.1% error rate
CAPACITY = 100000
ERROR_RATE = 0.001

# Initialize Bloom Filter
bloom = BloomFilter(capacity=CAPACITY, error_rate=ERROR_RATE)


def load_usernames():
    if os.path.exists("usernames.txt"):
        with open("usernames.txt", "r") as f:
            for line in f:
                # Adding directly to bloom - it handles hashing internally
                bloom.add(line.strip().lower())


# Load data on startup
load_usernames()


def generate_suggestions(base_name, count=3):
    suggestions = set()
    suffixes = ["_dev", "x", "_pro", "2026", "real"]

    attempts = 0
    while len(suggestions) < count and attempts < 100:
        attempts += 1
        candidate = f"{base_name}{random.choice(suffixes)}{random.randint(10, 99)}"

        # If Bloom filter says it's NOT there, it's 100% available
        if candidate not in bloom:
            suggestions.add(candidate)
    return list(suggestions)


@app.route("/check", methods=["POST"])
def check_username():
    data = request.json
    username = data.get("username", "").strip().lower()

    if len(username) < 3:
        return jsonify({"error": "Too short"}), 400

    # The probabilistic check
    is_taken = username in bloom

    response = {
        "exists": is_taken,
        "message": "Probably taken" if is_taken else "Definitely available"
    }

    if is_taken:
        response["suggestions"] = generate_suggestions(username)

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5050)