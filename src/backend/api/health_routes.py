# File: api/health_routes.py

from flask import Blueprint, jsonify
from utils.env_config import list_effective_config

health_api_bp = Blueprint('health_api_bp', __name__)


@health_api_bp.route('/config/info', methods=['GET'])
def config_info():
    """Return non-secret config values and their source."""
    return jsonify(list_effective_config()), 200
