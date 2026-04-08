import pytest
from v2_one.models.ollama_client import (
    get_embeddings,
    restructure_query,
    generate_answer,
)


def test_get_embeddings(mocker):
    # Mock the client.embed method
    mock_client = mocker.patch("v2_one.models.ollama_client.client")

    # Mock response for client.embed
    mock_response = mocker.Mock()
    mock_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_client.embed.return_value = mock_response

    embeddings = get_embeddings(["test text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.1, 0.2, 0.3]
    mock_client.embed.assert_called_once()


def test_get_embeddings_fallback(mocker):
    # Mock the client methods
    mock_client = mocker.patch("v2_one.models.ollama_client.client")

    # client.embed fails
    mock_client.embed.side_effect = Exception("Batch failed")

    # client.embeddings succeeds
    mock_response = mocker.Mock()
    mock_response.embedding = [0.4, 0.5, 0.6]
    mock_client.embeddings.return_value = mock_response

    embeddings = get_embeddings(["fallback text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.4, 0.5, 0.6]
    mock_client.embed.assert_called_once()
    mock_client.embeddings.assert_called_once()


def test_restructure_query(mocker):
    mock_client = mocker.patch("v2_one.models.ollama_client.client")

    mock_response = mocker.Mock()
    mock_response.response = "Optimized Query"
    mock_client.generate.return_value = mock_response

    result = restructure_query("What is RAG?")

    assert result == "Optimized Query"
    mock_client.generate.assert_called_once()


def test_generate_answer(mocker):
    mock_client = mocker.patch("v2_one.models.ollama_client.client")

    mock_response = mocker.Mock()
    mock_response.response = "This is the answer."
    mock_client.generate.return_value = mock_response

    result = generate_answer("Prompt text")

    assert result == "This is the answer."
    mock_client.generate.assert_called_once()
