from fastapi import APIRouter, Depends, HTTPException
from rag.api.dependencies import get_evaluation_service
from rag.api.schemas import EvaluationRequest, EvaluationResponse
from rag.services.evaluation import EvaluationService

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])


@router.post("/", response_model=EvaluationResponse)
async def run_evaluation(
    request: EvaluationRequest,
    evaluation_service: EvaluationService = Depends(get_evaluation_service),
):
    """
    Run a RAGAS evaluation on a given golden set.
    """
    try:
        result = await evaluation_service.evaluate(dataset_path=request.dataset_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
