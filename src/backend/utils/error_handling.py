# File: error_handling.py

from flask import jsonify


def handle_internal_server_error(e):
    return jsonify(error=str(e), status_code=500)


def handle_error_response(error_message, status_code):
    return jsonify({'error': error_message}), status_code
