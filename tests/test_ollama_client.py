import pytest
from v2_one.models.ollama_client import (
    get_embeddings,
    restructure_query,
    generate_answer,
)


def test_get_embeddings(mocker):
    # Mock httpx.Client.post
    mock_post = mocker.patch("httpx.Client.post")

    # Mock for successful /api/embed
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"embeddings": [[0.1, 0.2, 0.3]]}
    mock_post.return_value = mock_response

    embeddings = get_embeddings(["test text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.1, 0.2, 0.3]
    # Check it was called with /api/embed
    args, kwargs = mock_post.call_args
    assert "/api/embed" in args[0]


def test_get_embeddings_fallback(mocker):
    # Mock httpx.Client.post to fail on /api/embed but succeed on /api/embeddings
    mock_post = mocker.patch("httpx.Client.post")

    # First response (embed) is 404, second (embeddings) is 200
    mock_resp_embed = mocker.Mock()
    mock_resp_embed.status_code = 404

    mock_resp_embeddings = mocker.Mock()
    mock_resp_embeddings.status_code = 200
    mock_resp_embeddings.json.return_value = {"embedding": [0.4, 0.5, 0.6]}
    mock_resp_embeddings.raise_for_status = mocker.Mock()

    mock_post.side_effect = [mock_resp_embed, mock_resp_embeddings]

    embeddings = get_embeddings(["fallback text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.4, 0.5, 0.6]
    assert mock_post.call_count == 2


def test_restructure_query(mocker):
    mock_post = mocker.patch("httpx.Client.post")
    mock_post.return_value.json.return_value = {"response": "Optimized Query"}
    mock_post.return_value.raise_for_status = mocker.Mock()

    result = restructure_query("What is RAG?")

    assert result == "Optimized Query"
    mock_post.assert_called_once()


def test_generate_answer(mocker):
    mock_post = mocker.patch("httpx.Client.post")
    mock_post.return_value.json.return_value = {"response": "This is the answer."}
    mock_post.return_value.raise_for_status = mocker.Mock()

    result = generate_answer("Prompt text")

    assert result == "This is the answer."
    mock_post.assert_called_once()
