from typing import Any, Dict, List

from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

stores: List[Dict[str, Any]] = [
    {
        "name": "My Store",
        "items": [
            {"name": "Book", "price": 17.00},
            {"name": "Chair", "price": 97.70},
        ],
    }
]


@app.route("/")
def home():
    return render_template("index.html")


# POST /store data: {name:}
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)


# POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name: str):
    for store in stores:
        if store["name"] == name:
            request_data = request.get_json()
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"],
            }
            store["items"].append(new_item)
            return jsonify(new_item)
    return "what", 400


# GET /store/<string:name>
@app.route("/store/<string:name>")
def get_store(name: str):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return f"Store '{name}' not found.", 404


# GET /stores
@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})


# GET /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item")
def get_items_in_store(name: str):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]}), 200
    return jsonify({"message": "store not found"}), 404


app.run(port=5000)
