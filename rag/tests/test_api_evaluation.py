from fastapi.testclient import TestClient
from rag.main import app
from rag.api.dependencies import get_evaluation_service
from unittest.mock import AsyncMock

client = TestClient(app)


def test_evaluate_endpoint_success():
    mock_service = AsyncMock()
    mock_service.evaluate.return_value = {
        "status": "success",
        "md_report": "report.md",
        "csv_report": "report.csv",
        "metrics": {"faithfulness": 0.9},
    }
    app.dependency_overrides[get_evaluation_service] = lambda: mock_service

    response = client.post("/evaluate/", json={"dataset_path": "dummy.json"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["metrics"]["faithfulness"] == 0.9
