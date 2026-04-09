import os
import asyncio
import nest_asyncio
import typing as t
from typing import List, Dict, Any
from openai import AsyncOpenAI
import instructor
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas.llms.base import InstructorLLM, InstructorModelArgs
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig

# Use legacy metrics classes
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas import evaluate
from datasets import Dataset
from rag.utils.logger import logger
from rag.rag.pipeline import run_rag_pipeline
from rag.utils.llm_robustness import clean_json_response

# Allow nested event loops for RAGAS
nest_asyncio.apply()


def wrap_with_robust_cleaning(original_create):
    """
    Higher-order function to wrap the chat.completions.create method.
    """

    async def robust_create(*args, **kwargs):
        response = await original_create(*args, **kwargs)

        # Intercept and clean the raw response content
        if hasattr(response, "choices") and len(response.choices) > 0:
            content = response.choices[0].message.content
            if content:
                cleaned = clean_json_response(content)
                if cleaned != content:
                    logger.debug(
                        "Robustness: Cleaned raw JSON response before parsing."
                    )
                    response.choices[0].message.content = cleaned

        return response

    return robust_create


def get_ragas_llm():
    llm_model = os.getenv("EVAL_MODEL", "llama3.1:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    logger.info(f"Using {llm_model} as the RAGAS evaluation judge (Robust Mode).")

    # 1. Create Raw Client
    raw_client = AsyncOpenAI(base_url=f"{base_url}/v1", api_key="ollama")

    # 2. Monkey-patch the raw client's completions.create method
    original_create = raw_client.chat.completions.create
    raw_client.chat.completions.create = wrap_with_robust_cleaning(original_create)

    # 3. Patch with Instructor
    patched_client = instructor.from_openai(raw_client, mode=instructor.Mode.JSON)

    # 4. Wrap in RAGAS InstructorLLM
    return InstructorLLM(
        client=patched_client,
        model=llm_model,
        provider="openai",
        model_args=InstructorModelArgs(),
    )


def get_ragas_embeddings():
    embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    # Use native Langchain OllamaEmbeddings
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=base_url)
    # Wrap it for RAGAS legacy compatibility
    return LangchainEmbeddingsWrapper(embeddings)


def run_ragas_evaluation(questions, answers, contexts, ground_truths=None):
    """
    Run RAGAS evaluation on a set of results.
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

    # Configure legacy metrics
    faithfulness.llm = llm
    answer_relevancy.llm = llm
    answer_relevancy.embeddings = embeddings
    context_precision.llm = llm

    metrics = [faithfulness, answer_relevancy, context_precision]

    logger.info("Starting RAGAS evaluation...")

    run_config = RunConfig(timeout=500, max_retries=3)

    result = evaluate(
        dataset,
        metrics=metrics,
        run_config=run_config,
        batch_size=1,
        show_progress=True,
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
