from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/location', methods=['POST'])
def location():
    data = request.json

    lat = data.get('lat')
    lon = data.get('lon')

    print(f"\n📍 Phone Location Received:")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)