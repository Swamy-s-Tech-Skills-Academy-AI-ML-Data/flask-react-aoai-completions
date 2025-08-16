from flask import Blueprint, request, jsonify
from services.azure_openai_service import fetch_completion_response

completions_api_bp = Blueprint("completions_api_bp", __name__)


MAX_PROMPT_CHARS = 4000


@completions_api_bp.route("/completions", methods=["POST"])
def generate_completion():
    """Generate a single-turn completion.
    Request JSON: {"prompt": "..."}
    Response JSON: {"response": "...", "usage": {...}} (usage minimal placeholder for now)
    """
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "'prompt' is required"}), 400
    if len(prompt) > MAX_PROMPT_CHARS:
        return jsonify({"error": f"Prompt too long. Max {MAX_PROMPT_CHARS} characters."}), 400

    completion_text = fetch_completion_response(prompt)
    if completion_text.startswith("Error:"):
        return jsonify({"error": completion_text[6:].strip()}), 500

    return jsonify({
        "response": completion_text,
        "usage": {"prompt_chars": len(prompt), "response_chars": len(completion_text)}
    })
