import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Service URLs are injected via environment variables.
# Locally they default to localhost; in Docker/K8s they point at service names.
USERS_URL = os.environ.get("USERS_URL", "http://localhost:5001")
PRODUCTS_URL = os.environ.get("PRODUCTS_URL", "http://localhost:5002")

# In-memory order store.
ORDERS = []


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "orders"})


@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(ORDERS)


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(force=True)
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    # 1) Validate the user by calling the users-service.
    user_resp = requests.get(f"{USERS_URL}/users/{user_id}", timeout=5)
    if user_resp.status_code != 200:
        return jsonify({"error": "invalid user"}), 400
    user = user_resp.json()

    # 2) Validate the product by calling the products-service.
    product_resp = requests.get(f"{PRODUCTS_URL}/products/{product_id}", timeout=5)
    if product_resp.status_code != 200:
        return jsonify({"error": "invalid product"}), 400
    product = product_resp.json()

    # 3) Create the order from data gathered across both services.
    order = {
        "order_id": len(ORDERS) + 1,
        "user": user["name"],
        "product": product["name"],
        "price": product["price"],
    }
    ORDERS.append(order)
    return jsonify(order), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port)
