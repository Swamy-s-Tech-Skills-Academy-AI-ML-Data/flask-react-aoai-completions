# File: home_routes.py

import os
from flask import Blueprint, current_app, jsonify, send_from_directory

home_api_bp = Blueprint('home_api_bp', __name__)

# Define a route for the blueprint


# Routes: http://127.0.0.1:5009 OR http://127.0.0.1:5009/api
@home_api_bp.route('/', methods=['GET'])
def home():
    current_app.logger.info("Processing request to home route")

    # Simulate an error by raising an exception
    # raise Exception("This is a simulated error")

    return jsonify({'data': 'Welcome to Chat Completions - Python Flask API!'}), 200


@home_api_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(home_api_bp.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
