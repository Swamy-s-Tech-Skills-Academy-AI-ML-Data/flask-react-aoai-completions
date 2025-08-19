# File: api/config_routes.py

from flask import Blueprint, jsonify
from utils.env_config import list_effective_config

config_api_bp = Blueprint('config_api_bp', __name__)


@config_api_bp.route('/config/info', methods=['GET'])
def config_info():
    """Return non-secret config values and their source."""
    return jsonify(list_effective_config()), 200
