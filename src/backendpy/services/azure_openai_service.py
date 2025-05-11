import os
from openai import AzureOpenAI
from utils.env_config import get_config_value

# Load environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY_V1")
endpoint = get_config_value("AZURE_OPENAI_ENDPOINT")
deployment_name = get_config_value("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = get_config_value(
    "AZURE_OPENAI_API_VERSION")  # ✅ Now correctly loaded

if not api_key or not endpoint or not deployment_name or not api_version:
    raise ValueError("Azure OpenAI environment variables are missing!")

# ✅ Correct Azure OpenAI client setup (Synchronous)
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,  # ✅ Corrected
    api_version=api_version   # ✅ Added required api_version
)


def fetch_completion_response(prompt):
    """
    Calls Azure OpenAI API synchronously and yields responses.
    """
    chat_prompt = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False  # ✅ Disable streaming for synchronous processing
        )

        # ✅ Print response for debugging
        print(response)

        # ✅ Yield response text chunk-by-chunk
        if response.choices:
            # ✅ Get full response as a single chunk
            yield response.choices[0].message.content

    except Exception as e:
        yield f"Error: {str(e)}"
