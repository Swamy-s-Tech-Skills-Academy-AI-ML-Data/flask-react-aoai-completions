import os
import pytest

# Ensure test env variables (minimal) so import doesn't fail
os.environ.setdefault("AZURE_OPENAI_API_KEY_V1", "test-key")

# Provide dummy .env values matching code expectations
with open('.env', 'a', encoding='utf-8') as f:
    if 'AZURE_OPENAI_ENDPOINT' not in open('.env', 'r', encoding='utf-8').read():
        f.write('\nAZURE_OPENAI_ENDPOINT="https://test-endpoint.openai.azure.com"')
    if 'AZURE_OPENAI_DEPLOYMENT_NAME' not in open('.env', 'r', encoding='utf-8').read():
        f.write('\nAZURE_OPENAI_DEPLOYMENT_NAME="fake-deployment"')
    if 'AZURE_OPENAI_API_VERSION' not in open('.env', 'r', encoding='utf-8').read():
        f.write('\nAZURE_OPENAI_API_VERSION="2024-05-01-preview"')

# Monkeypatch AzureOpenAI client before app import


@pytest.fixture(autouse=True)
def mock_openai(monkeypatch):
    class DummyChoice:
        def __init__(self):
            class Msg:
                pass
            self.message = Msg()
            self.message.content = "Test completion response"

    class DummyResponse:
        def __init__(self):
            self.choices = [DummyChoice()]

    class DummyChatCompletions:
        def create(self, **kwargs):
            return DummyResponse()

    import os
    import pytest
    import importlib

    # Standardize env variable naming the code expects
    os.environ.setdefault("AZURE_OPENAI_API_KEY_V1", "test-key")
    os.environ.setdefault("AZURE_OPENAI_ENDPOINT",
                          "https://test-endpoint.openai.azure.com")
    os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT_NAME", "fake-deployment")
    os.environ.setdefault("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")

    class _DummyChoice:
        def __init__(self):
            class Msg:
                ...
            self.message = Msg()
            self.message.content = "Test completion response"

    class _DummyResponse:
        def __init__(self):
            self.choices = [_DummyChoice()]

    class _DummyChatCompletions:
        def create(self, **kwargs):
            return _DummyResponse()

    class _DummyChat:
        def __init__(self):
            self.completions = _DummyChatCompletions()

    class _DummyClient:
        def __init__(self, *args, **kwargs):
            self.chat = _DummyChat()

    @pytest.fixture(autouse=True)
    def mock_openai(monkeypatch):
        # Patch the class used for instantiation
        monkeypatch.setattr(
            'services.azure_openai_service.AzureOpenAI', _DummyClient, raising=False)
        # Reload module to rebuild the client with dummy
        import services.azure_openai_service as svc
        importlib.reload(svc)
        # Ensure its client is our dummy
        monkeypatch.setattr(svc, 'client', _DummyClient())
        yield

    @pytest.fixture
    def app():
        from app import create_app
        return create_app()

    @pytest.fixture
    def client(app):
        return app.test_client()
