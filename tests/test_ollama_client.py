import pytest
from v2_one.models.ollama_client import (
    get_embeddings,
    restructure_query,
    generate_answer,
)


def test_get_embeddings(mocker):
    # Mock httpx.Client.post
    mock_post = mocker.patch("httpx.Client.post")
    mock_post.return_value.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
    mock_post.return_value.raise_for_status = mocker.Mock()

    embeddings = get_embeddings(["test text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.1, 0.2, 0.3]
    mock_post.assert_called_once()


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
