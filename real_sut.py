from flask import Flask, request, jsonify
app = Flask(__name__)

loans = [
    {"id": 1, "user_id": "alice", "amount": 5000, "approved": True},
    {"id": 2, "user_id": "bob", "amount": 20000, "approved": False}
]

@app.route('/loans/<int:lid>', methods=['GET'])
def get_loan(lid):
    for loan in loans:
        if loan["id"] == lid:
            return jsonify(loan), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    if not data or "user_id" not in data or "amount" not in data:
        return jsonify({"error": "Missing user_id or amount"}), 400
    new_id = max([l["id"] for l in loans]) + 1
    approved = data["amount"] <= 10000
    new_loan = {"id": new_id, "user_id": data["user_id"], "amount": data["amount"], "approved": approved}
    loans.append(new_loan)
    return jsonify(new_loan), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)