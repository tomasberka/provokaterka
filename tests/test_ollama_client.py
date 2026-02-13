"""
Tests for OllamaClient.
"""

import pytest
from unittest.mock import patch, MagicMock
from ollama_client import OllamaClient


class TestOllamaClientInit:
    """Test OllamaClient initialization."""

    def test_default_init(self):
        """Test default initialization values."""
        client = OllamaClient()
        assert client.base_url == "http://localhost:11434"
        assert client.model == "llama3.2"
        assert client.temperature == 0.8

    def test_custom_init(self):
        """Test custom initialization values."""
        client = OllamaClient(
            base_url="http://example.com:8080/",
            model="mistral",
            temperature=0.5
        )
        assert client.base_url == "http://example.com:8080"
        assert client.model == "mistral"
        assert client.temperature == 0.5

    def test_base_url_trailing_slash_removed(self):
        """Test that trailing slash is removed from base_url."""
        client = OllamaClient(base_url="http://localhost:11434/")
        assert client.base_url == "http://localhost:11434"


class TestOllamaClientIsAvailable:
    """Test is_available method."""

    @patch("ollama_client.requests.get")
    def test_is_available_returns_true_on_200(self, mock_get):
        """Test is_available returns True when server responds 200."""
        mock_get.return_value.status_code = 200
        client = OllamaClient()
        assert client.is_available() is True
        mock_get.assert_called_once_with(
            "http://localhost:11434/api/tags", timeout=5
        )

    @patch("ollama_client.requests.get")
    def test_is_available_returns_false_on_non_200(self, mock_get):
        """Test is_available returns False when server responds non-200."""
        mock_get.return_value.status_code = 500
        client = OllamaClient()
        assert client.is_available() is False

    @patch("ollama_client.requests.get")
    def test_is_available_returns_false_on_connection_error(self, mock_get):
        """Test is_available returns False on connection error."""
        import requests
        mock_get.side_effect = requests.ConnectionError()
        client = OllamaClient()
        assert client.is_available() is False

    @patch("ollama_client.requests.get")
    def test_is_available_returns_false_on_timeout(self, mock_get):
        """Test is_available returns False on timeout."""
        import requests
        mock_get.side_effect = requests.Timeout()
        client = OllamaClient()
        assert client.is_available() is False


class TestOllamaClientGetModels:
    """Test get_models method."""

    @patch("ollama_client.requests.get")
    def test_get_models_returns_list_on_success(self, mock_get):
        """Test get_models returns list of model names."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3.2"},
                {"name": "mistral"},
                {"name": "codellama"}
            ]
        }
        mock_get.return_value = mock_response
        
        client = OllamaClient()
        models = client.get_models()
        
        assert models == ["llama3.2", "mistral", "codellama"]

    @patch("ollama_client.requests.get")
    def test_get_models_returns_empty_list_on_non_200(self, mock_get):
        """Test get_models returns empty list on non-200 response."""
        mock_get.return_value.status_code = 500
        client = OllamaClient()
        assert client.get_models() == []

    @patch("ollama_client.requests.get")
    def test_get_models_returns_empty_list_on_connection_error(self, mock_get):
        """Test get_models returns empty list on connection error."""
        import requests
        mock_get.side_effect = requests.ConnectionError()
        client = OllamaClient()
        assert client.get_models() == []

    @patch("ollama_client.requests.get")
    def test_get_models_returns_empty_list_on_invalid_json(self, mock_get):
        """Test get_models returns empty list on invalid JSON."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")
        client = OllamaClient()
        assert client.get_models() == []

    @patch("ollama_client.requests.get")
    def test_get_models_handles_empty_models_list(self, mock_get):
        """Test get_models handles empty models list."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": []}
        mock_get.return_value = mock_response
        
        client = OllamaClient()
        assert client.get_models() == []


class TestOllamaClientGenerate:
    """Test generate method."""

    @patch("ollama_client.requests.post")
    def test_generate_returns_response_on_success(self, mock_post):
        """Test generate returns response text on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "  Hello, world!  "}
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        result = client.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say hello"
        )
        
        assert result == "Hello, world!"
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"]["model"] == "llama3.2"
        assert call_kwargs[1]["json"]["prompt"] == "Say hello"
        assert call_kwargs[1]["json"]["system"] == "You are a helpful assistant."
        assert call_kwargs[1]["json"]["stream"] is False

    @patch("ollama_client.requests.post")
    def test_generate_uses_custom_max_tokens(self, mock_post):
        """Test generate uses custom max_tokens."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test"}
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        client.generate(
            system_prompt="test",
            user_prompt="test",
            max_tokens=100
        )
        
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"]["options"]["num_predict"] == 100

    @patch("ollama_client.requests.post")
    def test_generate_returns_none_on_non_200(self, mock_post):
        """Test generate returns None on non-200 response."""
        mock_post.return_value.status_code = 500
        client = OllamaClient()
        result = client.generate(
            system_prompt="test",
            user_prompt="test"
        )
        assert result is None

    @patch("ollama_client.requests.post")
    def test_generate_returns_none_on_connection_error(self, mock_post):
        """Test generate returns None on connection error."""
        import requests
        mock_post.side_effect = requests.ConnectionError()
        client = OllamaClient()
        result = client.generate(
            system_prompt="test",
            user_prompt="test"
        )
        assert result is None

    @patch("ollama_client.requests.post")
    def test_generate_returns_none_on_timeout(self, mock_post):
        """Test generate returns None on timeout."""
        import requests
        mock_post.side_effect = requests.Timeout()
        client = OllamaClient()
        result = client.generate(
            system_prompt="test",
            user_prompt="test"
        )
        assert result is None

    @patch("ollama_client.requests.post")
    def test_generate_returns_none_on_invalid_json(self, mock_post):
        """Test generate returns None on invalid JSON response."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.side_effect = ValueError("Invalid JSON")
        client = OllamaClient()
        result = client.generate(
            system_prompt="test",
            user_prompt="test"
        )
        assert result is None

    @patch("ollama_client.requests.post")
    def test_generate_handles_missing_response_key(self, mock_post):
        """Test generate handles missing response key gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        result = client.generate(
            system_prompt="test",
            user_prompt="test"
        )
        assert result == ""


class TestOllamaClientChat:
    """Test chat method."""

    @patch("ollama_client.requests.post")
    def test_chat_returns_response_on_success(self, mock_post):
        """Test chat returns response content on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"content": "  Hello from chat!  "}
        }
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        result = client.chat(
            messages=[{"role": "user", "content": "Hello"}],
            system_prompt="You are a helpful assistant."
        )
        
        assert result == "Hello from chat!"

    @patch("ollama_client.requests.post")
    def test_chat_includes_system_prompt_in_messages(self, mock_post):
        """Test chat includes system prompt as first message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Test"}}
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        client.chat(
            messages=[{"role": "user", "content": "Hello"}],
            system_prompt="System instruction"
        )
        
        call_kwargs = mock_post.call_args
        messages = call_kwargs[1]["json"]["messages"]
        assert messages[0] == {"role": "system", "content": "System instruction"}
        assert messages[1] == {"role": "user", "content": "Hello"}

    @patch("ollama_client.requests.post")
    def test_chat_without_system_prompt(self, mock_post):
        """Test chat works without system prompt."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Test"}}
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        client.chat(messages=[{"role": "user", "content": "Hello"}])
        
        call_kwargs = mock_post.call_args
        messages = call_kwargs[1]["json"]["messages"]
        assert len(messages) == 1
        assert messages[0] == {"role": "user", "content": "Hello"}

    @patch("ollama_client.requests.post")
    def test_chat_returns_none_on_non_200(self, mock_post):
        """Test chat returns None on non-200 response."""
        mock_post.return_value.status_code = 500
        client = OllamaClient()
        result = client.chat(messages=[{"role": "user", "content": "Hello"}])
        assert result is None

    @patch("ollama_client.requests.post")
    def test_chat_returns_none_on_connection_error(self, mock_post):
        """Test chat returns None on connection error."""
        import requests
        mock_post.side_effect = requests.ConnectionError()
        client = OllamaClient()
        result = client.chat(messages=[{"role": "user", "content": "Hello"}])
        assert result is None

    @patch("ollama_client.requests.post")
    def test_chat_returns_none_on_timeout(self, mock_post):
        """Test chat returns None on timeout."""
        import requests
        mock_post.side_effect = requests.Timeout()
        client = OllamaClient()
        result = client.chat(messages=[{"role": "user", "content": "Hello"}])
        assert result is None

    @patch("ollama_client.requests.post")
    def test_chat_handles_missing_message_key(self, mock_post):
        """Test chat handles missing message key gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        client = OllamaClient()
        result = client.chat(messages=[{"role": "user", "content": "Hello"}])
        assert result == ""
