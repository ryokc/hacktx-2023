from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

purchases = []  # Initialize an empty list

@app.route("/purchases", methods=['GET'])
def get_purchases():
    return jsonify({"purchases": purchases})

@app.route("/add_purchase", methods=['POST'])
def add_purchase():
    data = request.get_json()
    new_purchase = data.get('purchase')
    purchases.append(new_purchase)
    return jsonify({"message": "Purchase added successfully"})

if __name__ == "__main__":
    app.run(debug=True)