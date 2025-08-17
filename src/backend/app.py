# File: app.py

import os
from flask import Flask, jsonify
from flask_cors import CORS

from api.home_routes import home_api_bp
from utils.logging_config import configure_logging
from api.completions_routes import completions_api_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Ensure logs directory exists relative to backend root
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    def handle_custom_error(e):
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response

    # Configure logging (guard against duplicate handlers on reload)
    configure_logging(app)
    app.register_error_handler(Exception, handle_custom_error)

    # Blueprints
    app.register_blueprint(home_api_bp, name='home_route_direct')
    app.register_blueprint(home_api_bp, url_prefix='/api')
    app.register_blueprint(completions_api_bp, url_prefix='/api')

    app.logger.info("Starting Chat Completions API")
    return app


# # Create the app and run it during development (.\app.py)
if __name__ == "__main__":
    print("Starting Python Flask Server For Chat Completions API")
    app = create_app()
    app.run(host='0.0.0.0', port=5009, debug=True)

# # For production deployment, comment out the above lines and use the one below (Flask run)
# # This can also be used for development while running the app from Debug mode in VS Code
# print("Starting Python Flask Server For Chat Completions API using Flask run")
# app = create_app()
# app.run()  # In production
