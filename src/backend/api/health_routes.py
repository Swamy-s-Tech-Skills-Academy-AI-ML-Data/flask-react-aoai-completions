"""
Deprecated routes kept temporarily for compatibility.
Prefer using /api/config/info via config_routes.py
"""

from flask import Blueprint, jsonify

health_api_bp = Blueprint('health_api_bp', __name__)


@health_api_bp.route('/health/config', methods=['GET'])
def deprecated_health_config():
    return jsonify({
        'error': 'This endpoint is deprecated. Use /api/config/info instead.'
    }), 410
