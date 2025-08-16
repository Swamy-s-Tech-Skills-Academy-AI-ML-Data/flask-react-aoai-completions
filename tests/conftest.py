import os
import sys
import pathlib
import importlib
import pytest

ROOT = pathlib.Path(__file__).parent.parent.resolve()
BACKEND = ROOT / 'src' / 'backendpy'
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

# Ensure .env has required keys for dotenv-based config loader
env_file = ROOT / '.env'
existing = env_file.read_text(encoding='utf-8') if env_file.exists() else ''
required_pairs = {
    'AZURE_OPENAI_ENDPOINT': 'https://test-endpoint.openai.azure.com',
    'AZURE_OPENAI_DEPLOYMENT_NAME': 'fake-deployment',
    'AZURE_OPENAI_API_VERSION': '2024-05-01-preview'
}
lines_to_append = []
for k, v in required_pairs.items():
    if k not in existing:
        lines_to_append.append(f'{k}="{v}"')
if lines_to_append:
    env_file.write_text((existing + ('\n' if not existing.endswith('\n')
                        else '') + '\n'.join(lines_to_append)), encoding='utf-8')

# Also provide both key name variants
os.environ.setdefault('AZURE_OPENAI_API_KEY_V1', 'test-key')
os.environ.setdefault('AZURE_OPENAI_API_KEY', 'test-key')


class DummyChoice:
    def __init__(self):
        class Msg:
            ...
        self.message = Msg()
        self.message.content = 'Test completion response'


class DummyResponse:
    def __init__(self):
        self.choices = [DummyChoice()]


class DummyChatCompletions:
    def create(self, **kwargs):
        return DummyResponse()


class DummyChat:
    def __init__(self):
        self.completions = DummyChatCompletions()


class DummyClient:
    def __init__(self, *args, **kwargs):
        self.chat = DummyChat()


@pytest.fixture(autouse=True)
def patch_azure_openai(monkeypatch):
    # Patch class before (re)import
    monkeypatch.setattr(
        'services.azure_openai_service.AzureOpenAI', DummyClient, raising=False)
    import services.azure_openai_service as svc
    importlib.reload(svc)
    monkeypatch.setattr(svc, 'client', DummyClient())
    yield


@pytest.fixture
def app():
    from app import create_app
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()
