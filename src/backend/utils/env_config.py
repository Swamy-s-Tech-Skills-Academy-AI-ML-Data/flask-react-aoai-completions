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
