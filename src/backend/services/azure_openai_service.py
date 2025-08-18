import os
from openai import AzureOpenAI
from utils.env_config import get_config_value
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_client():
    """Build and cache Azure OpenAI client on first use."""
    # Support both key names; prefer explicit env config
    api_key = (os.getenv("AZURE_OPENAI_API_KEY_V1"))
    # print(f"Using Azure OpenAI API Key: {api_key}")

    endpoint = get_config_value(
        "AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = get_config_value(
        "AZURE_OPENAI_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = get_config_value(
        "AZURE_OPENAI_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION")

    if not all([api_key, endpoint, deployment_name, api_version]):
        raise RuntimeError(
            "Azure OpenAI configuration incomplete. Check environment variables.")

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version
    )
    # Persist deployment name on function attribute for reuse
    client._deployment_name = deployment_name
    return client


def fetch_completion_response(prompt: str) -> str:
    """Call Azure OpenAI and return the full completion text (single turn).

    Any exception (including configuration issues) is converted into a prefixed
    string so the route layer can produce a JSON error without invoking the
    global exception handler (preserving informative messages in dev).
    """
    try:
        client = _get_client()
        chat_prompt = [
            {"role": "system", "content": "You are an AI assistant that helps people find information."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model=client._deployment_name,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        )
        if response.choices:
            return response.choices[0].message.content
        return ""
    except Exception as e:  # Broad catch converts to controlled error string
        return f"Error: {e}"
