import os
from pathlib import Path
from dotenv import dotenv_values


def _load_root_env():
    # Walk up until .env is found (repo root) or stop at filesystem root
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent / '.env'
        if candidate.is_file():
            return dotenv_values(str(candidate))
    return {}


_CONFIG = _load_root_env()


def get_config_value(key: str):
    # Prefer already exported environment variables; fallback to loaded .env values
    return os.getenv(key) or _CONFIG.get(key)


def list_effective_config(include_secrets: bool = False):
    visible_keys = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_DEPLOYMENT_NAME',
        'AZURE_OPENAI_API_VERSION',
        'LOG_LEVEL',
        'LOG_FORMAT'
    ]
    out = {}
    for k in visible_keys:
        val_env = os.getenv(k)
        source = 'env' if val_env is not None else 'file' if k in _CONFIG else 'absent'
        value = val_env if val_env is not None else _CONFIG.get(k)
        out[k] = {'value': value, 'source': source}
    if include_secrets:
        for k in ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_API_KEY_V1']:
            if os.getenv(k):
                out[k] = {'value': '***MASKED***', 'source': 'env'}
            elif k in _CONFIG:
                out[k] = {'value': '***MASKED***', 'source': 'file'}
    return out
