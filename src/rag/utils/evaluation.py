import os
import asyncio
import nest_asyncio
from typing import List, Dict, Any
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Use legacy metrics classes
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas import evaluate
from datasets import Dataset
from rag.utils.logger import logger
from rag.rag.pipeline import run_rag_pipeline

# Allow nested event loops for RAGAS
nest_asyncio.apply()


def get_ragas_llm():
    llm_model = os.getenv("LLM_MODEL", "llama3.2")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return ChatOllama(model=llm_model, base_url=base_url)


def get_ragas_embeddings():
    embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return OllamaEmbeddings(model=embedding_model, base_url=base_url)


def run_ragas_evaluation(questions, answers, contexts, ground_truths=None):
    """
    Run RAGAS evaluation on a set of results using legacy (but functional) metrics.
    """
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    }
    if ground_truths:
        data["ground_truth"] = ground_truths

    dataset = Dataset.from_dict(data)

    llm = get_ragas_llm()
    embeddings = get_ragas_embeddings()

    ragas_llm = LangchainLLMWrapper(llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

    # Configure legacy metrics
    faithfulness.llm = ragas_llm
    answer_relevancy.llm = ragas_llm
    answer_relevancy.embeddings = ragas_embeddings
    context_precision.llm = ragas_llm

    metrics = [faithfulness, answer_relevancy, context_precision]

    logger.info("Starting RAGAS evaluation...")
    result = evaluate(
        dataset,
        metrics=metrics,
    )

    return result


async def run_comparative_evaluation(golden_set: List[Dict[str, str]]):
    """
    Run the golden set through 4 different configurations.
    Returns a dictionary of result sets.
    """
    configs = [
        {"restructure": False, "rescore": False, "name": "baseline"},
        {"restructure": True, "rescore": False, "name": "restructure_only"},
        {"restructure": False, "rescore": True, "name": "rescore_only"},
        {"restructure": True, "rescore": True, "name": "full"},
    ]

    results_by_config = {}

    for config in configs:
        logger.info(f"Evaluating configuration: {config['name']}...")
        mode_results = []
        for item in golden_set:
            rag_output = await run_rag_pipeline(
                item["question"],
                use_restructuring=config["restructure"],
                use_rescoring=config["rescore"],
            )
            mode_results.append(
                {
                    "question": item["question"],
                    "answer": rag_output["answer"],
                    "contexts": rag_output["contexts"],
                    "ground_truth": item["ground_truth"],
                }
            )
        results_by_config[config["name"]] = mode_results

    return results_by_config


async def calculate_comparative_metrics(
    results_by_config: Dict[str, List[Dict[str, Any]]]
):
    """
    Calculate RAGAS metrics for each configuration.
    """
    final_evaluation = {}

    for name, mode_results in results_by_config.items():
        logger.info(f"Calculating RAGAS metrics for {name}...")

        questions = [r["question"] for r in mode_results]
        answers = [r["answer"] for r in mode_results]
        contexts = [r["contexts"] for r in mode_results]
        ground_truths = [r["ground_truth"] for r in mode_results]

        # Run evaluation for this mode
        result = run_ragas_evaluation(questions, answers, contexts, ground_truths)
        final_evaluation[name] = result

    return final_evaluation
