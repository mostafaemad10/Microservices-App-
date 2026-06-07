import os
from flask import Flask, jsonify

app = Flask(__name__)

# In-memory "database" so we don't need a real DB for the DevOps demo.
USERS = {
    1: {"id": 1, "name": "Alice",   "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob",     "email": "bob@example.com"},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "users"})


@app.route("/users")
def list_users():
    return jsonify(list(USERS.values()))


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
