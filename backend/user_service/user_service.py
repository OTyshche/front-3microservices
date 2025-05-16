# user_service.py
from flask import Flask, jsonify
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes and origins

@app.route('/api/user', methods=['GET'])
def get_user_greeting():
    """
    Returns a simple greeting message.
    """
    return jsonify({"message": "Hello from the Python User Service!"})

if __name__ == '__main__':
    # It's good practice to make the host configurable,
    # especially for Docker. 0.0.0.0 makes it accessible externally.
    app.run(host='0.0.0.0', port=5001, debug=True)
