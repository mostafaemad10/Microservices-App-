import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_URL = os.environ.get("USERS_URL", "http://localhost:5001")
PRODUCTS_URL = os.environ.get("PRODUCTS_URL", "http://localhost:5002")
ORDERS_URL = os.environ.get("ORDERS_URL", "http://localhost:5003")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "gateway"})


@app.route("/")
def index():
    return jsonify({
        "service": "gateway",
        "endpoints": ["/users", "/products", "/orders", "/summary"],
    })


@app.route("/users")
def users():
    return jsonify(requests.get(f"{USERS_URL}/users", timeout=5).json())


@app.route("/products")
def products():
    return jsonify(requests.get(f"{PRODUCTS_URL}/products", timeout=5).json())


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        resp = requests.post(
            f"{ORDERS_URL}/orders", json=request.get_json(force=True), timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    return jsonify(requests.get(f"{ORDERS_URL}/orders", timeout=5).json())


@app.route("/summary")
def summary():
    # Aggregates data from all three downstream services in one call.
    users_count = len(requests.get(f"{USERS_URL}/users", timeout=5).json())
    products_count = len(requests.get(f"{PRODUCTS_URL}/products", timeout=5).json())
    orders_count = len(requests.get(f"{ORDERS_URL}/orders", timeout=5).json())
    return jsonify({
        "users": users_count,
        "products": products_count,
        "orders": orders_count,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
