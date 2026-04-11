import pytest
from unittest.mock import AsyncMock, MagicMock
from rag.models.ollama_client import (
    get_embeddings,
    restructure_query,
    generate_answer,
)


@pytest.mark.asyncio
async def test_get_embeddings(mocker):
    # Mock the client.embed method
    mock_client = mocker.patch(
        "rag.models.ollama_client.client", new_callable=AsyncMock
    )

    # Mock response for client.embed
    mock_response = MagicMock()
    mock_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_client.embed.return_value = mock_response

    embeddings = await get_embeddings(["test text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.1, 0.2, 0.3]
    mock_client.embed.assert_called_once()


@pytest.mark.asyncio
async def test_get_embeddings_fallback(mocker):
    # Mock the client methods
    mock_client = mocker.patch(
        "rag.models.ollama_client.client", new_callable=AsyncMock
    )

    # client.embed fails
    mock_client.embed.side_effect = Exception("Batch failed")

    # client.embeddings succeeds
    mock_response = MagicMock()
    mock_response.embedding = [0.4, 0.5, 0.6]
    mock_client.embeddings.return_value = mock_response

    embeddings = await get_embeddings(["fallback text"])

    assert len(embeddings) == 1
    assert embeddings[0] == [0.4, 0.5, 0.6]
    mock_client.embed.assert_called_once()
    mock_client.embeddings.assert_called_once()


@pytest.mark.asyncio
async def test_restructure_query(mocker):
    mock_client = mocker.patch(
        "rag.models.ollama_client.client", new_callable=AsyncMock
    )

    mock_response = {"message": {"content": "Optimized Query"}}
    mock_client.chat.return_value = mock_response

    result = await restructure_query("What is RAG?")

    assert result == "Optimized Query"
    mock_client.chat.assert_called_once()


@pytest.mark.asyncio
async def test_generate_answer(mocker):
    mock_client = mocker.patch(
        "rag.models.ollama_client.client", new_callable=AsyncMock
    )

    mock_response = MagicMock()
    mock_response.response = "This is the answer."
    mock_client.generate.return_value = mock_response

    result = await generate_answer("Prompt text")

    assert result == "This is the answer."
    mock_client.generate.assert_called_once()
