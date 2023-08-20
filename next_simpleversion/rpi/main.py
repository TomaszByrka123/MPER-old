from flask import Flask, request, jsonify

app = Flask(__name__)

current_data = {"value": "Initial Value"}

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(current_data)

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json
    if "value" in data:
        current_data["value"] = data["value"]
        return jsonify({"message": "Data updated"})
    else:
        return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
