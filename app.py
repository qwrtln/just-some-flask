from flask import Flask, jsonify, request, Response

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "Book", "price": 17.00}]}]


# POST /store data: {name:}
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route("/store/<string:name>")
def get_store(name: str):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return f"Store '{name}' not found.", 404


# GET /stores
@app.route("/stores")
def get_stores():
    return jsonify({"stores": stores})


app.run(port=5000)
