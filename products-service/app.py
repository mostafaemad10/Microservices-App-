import os
from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    101: {"id": 101, "name": "Laptop",     "price": 1200.00},
    102: {"id": 102, "name": "Headphones", "price": 150.00},
    103: {"id": 103, "name": "Coffee Mug", "price": 12.50},
}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "products"})


@app.route("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))


@app.route("/products/<int:product_id>")
def get_product(product_id):
    product = PRODUCTS.get(product_id)
    if not product:
        return jsonify({"error": "product not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
