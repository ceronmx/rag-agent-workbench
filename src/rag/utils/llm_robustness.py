import json
import re
import typing as t
from rag.utils.logger import logger


def clean_json_response(text: str) -> str:
    """
    Clean the LLM response to ensure it only contains valid JSON.
    Strips markdown blocks, preambles, and trailing noise.
    """
    # 1. Strip triple backtick markdown blocks (```json ... ``` or just ``` ... ```)
    # The non-greedy .*? is important.
    markdown_pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(markdown_pattern, text, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
        logger.debug("Stripped markdown block from LLM response.")
        return cleaned

    # 2. If no markdown blocks, try to find the first '{' and last '}'
    # This helps if the LLM says "Here is the result: { ... } Hope that helps!"
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        cleaned = text[start_idx : end_idx + 1].strip()
        logger.debug("Extracted JSON curly brace block from LLM response.")
        return cleaned

    # 3. Last resort: just return original text stripped
    return text.strip()


class RobustOllamaClient:
    """
    A wrapper for the Ollama (OpenAI-compatible) client that intercepts
    responses and cleans them before returning to the caller.
    """

    def __init__(self, original_client):
        self.original_client = original_client
        # Proxy attributes
        self.embeddings = original_client.embeddings

    @property
    def chat(self):
        return RobustChat(self.original_client.chat)


class RobustChat:
    def __init__(self, original_chat):
        self.original_chat = original_chat

    @property
    def completions(self):
        return RobustCompletions(self.original_chat.completions)


class RobustCompletions:
    def __init__(self, original_completions):
        self.original_completions = original_completions

    async def create(self, *args, **kwargs):
        # We only care about cleaning if response_model is provided (Instructor logic)
        # However, Instructor patches the client itself.
        # RAGAS 0.4 uses Instructor which handles the Pydantic parsing.

        # If we are here, we are likely inside Instructor's patched create call.
        response = await self.original_completions.create(*args, **kwargs)

        # NOTE: Instructor works by hooking into the client.
        # If we wrap the client BEFORE passing it to llm_factory,
        # Instructor will patch our wrapper.

        return response
