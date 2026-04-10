import os
from rag.utils.logger import logger
from rag.utils.datasets import load_golden_set
from rag.utils.evaluation import (
    run_comparative_evaluation,
    calculate_comparative_metrics,
)
from rag.utils.reporting import generate_evaluation_report
from rag.models.ollama_client import LLM_MODEL, EMBEDDING_MODEL


class EvaluationService:
    async def evaluate(self, dataset_path: str = "data/eval/golden_set.json"):
        logger.info(f"Loading golden set from {dataset_path}...")
        golden_set = load_golden_set(dataset_path)
        if not golden_set:
            logger.error("No evaluation data found.")
            raise ValueError(f"Evaluation data not found at {dataset_path}")

        # 1. Run RAG pipeline across configurations
        results_by_config = await run_comparative_evaluation(golden_set)

        # 2. Calculate Metrics
        final_metrics = await calculate_comparative_metrics(results_by_config)

        # 3. Generate Report
        md_report, csv_report = generate_evaluation_report(
            final_metrics, LLM_MODEL, EMBEDDING_MODEL
        )

        eval_model = os.getenv("EVAL_MODEL", "llama3.1:8b")
        logger.info(
            f"Evaluation complete. Reports generated at {md_report} and {csv_report} (Judge: {eval_model})"
        )

        return {
            "status": "success",
            "md_report": md_report,
            "csv_report": csv_report,
            "metrics": final_metrics,
        }
