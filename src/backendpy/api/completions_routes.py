from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.azure_openai_service import fetch_completion_response

completions_api_bp = Blueprint("completions_api_bp", __name__)


@completions_api_bp.route("/completions", methods=["POST"])
def generate_completion():
    """
    API endpoint for generating text completions.
    Expects a JSON request with {"prompt": "..."}.
    """
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400

    prompt = data["prompt"]

    return Response(
        stream_with_context(fetch_completion_response(prompt)),
        content_type="text/event-stream"
    )
