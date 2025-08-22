# File: app.py

import os
from flask import Flask
from flask_cors import CORS

from api.home_routes import home_api_bp
from api.completions_routes import completions_api_bp

from utils.logging_config import configure_logging
from utils.env_config import list_effective_config
from utils.error_handling import register_error_handlers


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Ensure logs directory exists relative to backend root
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging (guard against duplicate handlers on reload)
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Home routes
    app.register_blueprint(home_api_bp, name='home_route_direct')
    app.register_blueprint(home_api_bp, url_prefix='/api')

    # Config routes
    from api.config_routes import config_api_bp
    app.register_blueprint(
        config_api_bp, url_prefix='/api')  # /api/config/info

    # Completions routes
    app.register_blueprint(completions_api_bp, url_prefix='/api')

    # Log summarized non-secret config once
    cfg = list_effective_config()
    redacted_cfg = {k: {**v, 'value': (v['value'] if k not in (
        'AZURE_OPENAI_ENDPOINT',) else v['value'])} for k, v in cfg.items()}
    app.logger.info("Starting Chat Completions API | config=%s", redacted_cfg)
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
