import pandas as pd
import os
from datetime import datetime
from typing import Dict, Any
from rag.utils.logger import logger


def generate_evaluation_report(
    evaluation_results: Dict[str, Any], llm_model: str, embedding_model: str
):
    """
    Generate Markdown and CSV reports from evaluation results.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = "data/eval/reports"
    os.makedirs(report_dir, exist_ok=True)

    # Prepare data for summary
    summary_data = []
    for name, result in evaluation_results.items():
        row = {"configuration": name}
        try:
            # result is a Ragas EvaluationResult object
            # In RAGAS 0.4.x, the result object itself has the mean scores
            # if we iterate or convert to dict.
            for metric_name, score in result.items():
                row[metric_name] = score
        except Exception as e:
            # If evaluation failed or returned no scores
            logger.warning(f"Failed to extract metrics for {name}: {e}")
            row.update(
                {"faithfulness": 0.0, "answer_relevancy": 0.0, "context_precision": 0.0}
            )
        summary_data.append(row)

    df = pd.DataFrame(summary_data)

    # Save CSV
    csv_path = os.path.join(report_dir, f"evaluation_{timestamp}.csv")
    df.to_csv(csv_path, index=False)
    logger.info(f"CSV report saved to {csv_path}")

    # Generate Markdown
    md_path = os.path.join(report_dir, f"evaluation_{timestamp}.md")
    eval_model = os.getenv("EVAL_MODEL", "llama3.1:8b")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# RAG Evaluation Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Application Model:** `{llm_model}`\n")
        f.write(f"**Judge Model:** `{eval_model}`\n")
        f.write(f"**Embedding Model:** `{embedding_model}`\n\n")

        f.write("## Summary Metrics\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n## Observations\n")
        f.write(
            "- Compare the lift in metrics when enabling query restructuring and rescoring.\n"
        )

    logger.info(f"Markdown report saved to {md_path}")
    return md_path, csv_path
