# File: app.py

import os
from flask import Flask, jsonify, g
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from api.home_routes import home_api_bp
from utils.logging_config import configure_logging
from api.completions_routes import completions_api_bp
from utils.env_config import list_effective_config


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Ensure logs directory exists relative to backend root
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Distinguish HTTPException (use its code) vs generic exceptions
    def handle_generic_exception(e):
        app.logger.exception("Unhandled exception: %s", e)
        cid = getattr(g, 'correlation_id', None)
        # Allow explicit runtime misconfiguration messages to surface; mask others
        message = 'Internal server error'
        if isinstance(e, RuntimeError) and 'configuration incomplete' in str(e):
            message = str(e)
        body = {'error': message}
        if cid:
            body['correlation_id'] = cid
        return jsonify(body), 500

    def handle_http_exception(e: HTTPException):
        # Provide consistent JSON error response
        description = getattr(e, 'description', str(e))
        cid = getattr(g, 'correlation_id', None)
        body = {'error': description}
        if cid:
            body['correlation_id'] = cid
        return jsonify(body), getattr(e, 'code', 500)

    def handle_404(e: HTTPException):
        cid = getattr(g, 'correlation_id', None)
        body = {'error': 'Resource not found'}
        if cid:
            body['correlation_id'] = cid
        return jsonify(body), 404

    # Configure logging (guard against duplicate handlers on reload)
    configure_logging(app)
    # Register specific then generic
    app.register_error_handler(404, handle_404)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_generic_exception)

    # Blueprints
    app.register_blueprint(home_api_bp, name='home_route_direct')
    app.register_blueprint(home_api_bp, url_prefix='/api')
    app.register_blueprint(completions_api_bp, url_prefix='/api')

    # Log summarized non-secret config once
    cfg = list_effective_config()
    redacted_cfg = {k: {**v, 'value': (v['value'] if k not in ('AZURE_OPENAI_ENDPOINT',) else v['value'])} for k, v in cfg.items()}
    app.logger.info("Starting Chat Completions API | config=%s", redacted_cfg)

    @app.route('/api/health/config', methods=['GET'])
    def health_config():  # pragma: no cover simple utility
        return jsonify(list_effective_config()), 200
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
