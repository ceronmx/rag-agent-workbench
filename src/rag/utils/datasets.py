import json
import os
from typing import List, Dict, Any
from rag.utils.logger import logger

DEFAULT_EVAL_PATH = "data/eval/golden_set.json"


def save_golden_set(data: List[Dict[str, str]], file_path: str = DEFAULT_EVAL_PATH):
    """
    Save a list of questions and ground truths to a JSON file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(data)} items to {file_path}")


def load_golden_set(file_path: str = DEFAULT_EVAL_PATH) -> List[Dict[str, str]]:
    """
    Load a golden set from a JSON file.
    """
    if not os.path.exists(file_path):
        logger.warning(f"Golden set file not found: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info(f"Loaded {len(data)} items from {file_path}")
    return data


def create_sample_golden_set():
    """
    Create a sample golden set if none exists.
    """
    sample = [
        {
            "question": "What is pgvector?",
            "ground_truth": "pgvector is an open-source extension for PostgreSQL that allows you to store and search vector embeddings in your database. It supports exact and approximate nearest neighbor search, L2 distance, inner product, and cosine distance.",
        },
        {
            "question": "What are the benefits of using RAG?",
            "ground_truth": "Retrieval-Augmented Generation (RAG) improves LLM responses by providing specific, up-to-date context from external documents. It reduces hallucinations, allows for better attribution, and enables the model to answer questions about private or recent data without retraining.",
        },
    ]
    if not os.path.exists(DEFAULT_EVAL_PATH):
        save_golden_set(sample)
        return True
    return False
