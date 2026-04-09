import pytest
from unittest.mock import AsyncMock, MagicMock
from v2_one.rag.engine import rescore_results, assemble_rag_prompt
from dataclasses import dataclass


@dataclass
class MockResult:
    text: str
    document_name: str
    chunk_index: int
    similarity: float


@pytest.mark.asyncio
async def test_rescore_results_basic(mocker):
    # Setup mock results
    results = [
        MockResult("Apple", "fruits.pdf", 0, 0.9),
        MockResult("Banana", "fruits.pdf", 1, 0.8),
        MockResult("Cherry", "fruits.pdf", 2, 0.7),
    ]

    # Mock the client.generate method
    mock_client = mocker.patch("v2_one.rag.engine.client", new_callable=AsyncMock)

    mock_response = MagicMock()
    mock_response.response = "1, 0"
    mock_client.generate.return_value = mock_response

    rescored = await rescore_results("query about bananas", results)

    # Check if Banana is first now
    assert len(rescored) == 3
    assert rescored[0].text == "Banana"
    assert rescored[1].text == "Apple"
    assert (
        rescored[2].text == "Cherry"
    )  # Cherry was not in the list, so it's added at the end


@pytest.mark.asyncio
async def test_rescore_results_empty():
    assert await rescore_results("query", []) == []


@pytest.mark.asyncio
async def test_rescore_results_error(mocker):
    results = [MockResult("Apple", "fruits.pdf", 0, 0.9)]
    # Mock an error in the generate request
    mock_client = mocker.patch("v2_one.rag.engine.client", new_callable=AsyncMock)
    mock_client.generate.side_effect = Exception("API Error")

    # Should return original results on failure
    rescored = await rescore_results("query", results)
    assert rescored == results


def test_assemble_rag_prompt():
    results = [
        MockResult("Content 1", "doc1.pdf", 10, 0.95),
        MockResult("Content 2", "doc2.pdf", 5, 0.90),
    ]
    query = "What is the content?"

    prompt = assemble_rag_prompt(query, results, top_k=1)

    assert "Content 1" in prompt
    assert "doc1.pdf" in prompt
    assert "Chunk 10" in prompt
    assert "Content 2" not in prompt  # Because top_k=1
    assert query in prompt
    assert "CONTEXT:" in prompt
    assert "USER QUESTION:" in prompt
