from flask import Flask, jsonify

app = Flask(__name__)

# Simulated Product Database
PRODUCTS = [
    {"id": 1, "name": "Mechanical Keyboard", "price": 120.00, "description": "Clicky keys for maximum productivity."},
    {"id": 2, "name": "4K Monitor", "price": 350.50, "description": "Crystal clear visuals for coding and design."},
    {"id": 3, "name": "Ergonomic Mouse", "price": 45.00, "description": "Comfortable design for long sessions."}
]

@app.route('/products')
def get_products():
    """Returns the list of all products."""
    # This is the endpoint the frontend will call internally
    return jsonify(PRODUCTS)

@app.route('/status')
def status():
    """Returns service health status."""
    return jsonify({"service": "Catalog Service", "status": "UP"}), 200

if __name__ == '__main__':
    # Runs on port 5001 internally
    app.run(host='0.0.0.0', port=5001)
