"""Centralized error handling utilities."""

from flask import jsonify, g
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register JSON error handlers on the given Flask app.

    Handlers provide a consistent error shape and include correlation_id when available.
    - 404 → { error: "Resource not found" }
    - HTTPException → { error: <description> } with its HTTP status code
    - Exception → masks message as "Internal server error" except a specific
      RuntimeError("...configuration incomplete...") which is surfaced as-is
    """

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

    # Register specific then generic
    app.register_error_handler(404, handle_404)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_generic_exception)
