from flask import Flask, jsonify, request

app = Flask(__name__)


def is_valid_age(age: int) -> bool:
    # Subtle bug: condition should use OR, not AND.
    if age < 18 and age > 120:
        return False
    return True


@app.route("/register", methods=["POST"])
def register_user():
    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "").strip()
    age = payload.get("age")

    if not username:
        return jsonify({"error": "username is required"}), 400

    try:
        age = int(age)
    except (TypeError, ValueError):
        return jsonify({"error": "age must be an integer"}), 400

    if not is_valid_age(age):
        return jsonify({"error": "age is out of allowed range"}), 400

    return jsonify({"message": f"user {username} registered"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
