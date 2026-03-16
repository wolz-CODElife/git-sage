"""
ollama.py
---------
Thin HTTP client for the Ollama local inference server.

Ollama exposes a REST API on http://localhost:11434 by default.
We use httpx (sync) to keep the dependency footprint small.

Reference: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

import json
import sys
from typing import Iterator, Optional

import httpx

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5-coder:7b"

# How long to wait for the first token (seconds).
# Code review of a large diff can take 20-30 s on CPU.
TIMEOUT = 120


class OllamaError(Exception):
    """Raised when the Ollama server returns an error or is unreachable."""


def is_available(host: str = DEFAULT_HOST) -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        r = httpx.get(f"{host}/api/tags", timeout=3)
        return r.status_code == 200
    except httpx.RequestError:
        return False


def list_models(host: str = DEFAULT_HOST) -> list[str]:
    """Return the names of locally available models."""
    try:
        r = httpx.get(f"{host}/api/tags", timeout=5)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except httpx.RequestError as exc:
        raise OllamaError(f"Cannot reach Ollama at {host}: {exc}") from exc


def _select_fallback_model(requested_model: str, available_models: list[str]) -> Optional[str]:
    """
    Select a fallback model from available models.
    
    Strategy:
    1. If requested_model is in available_models, return None (no fallback needed)
    2. Otherwise, return the first available model
    3. If no models available, return None
    """
    if requested_model in available_models:
        return None
    
    if not available_models:
        return None
    
    return available_models[0]


def chat(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_HOST,
    stream: bool = False,
    fallback: bool = True,
) -> str | Iterator[str]:
    """
    Send a chat request to Ollama.

    Parameters
    ----------
    messages:
        List of {"role": ..., "content": ...} dicts (OpenAI-compatible).
    model:
        Local model name, e.g. "qwen2.5-coder:7b".
    host:
        Ollama server base URL.
    stream:
        If True, yield text chunks as they arrive (for live output).
        If False (default), return the complete response string.
    fallback:
        If True (default), fall back to another available model if requested
        model is not available locally. If False, raise an error immediately.

    Returns
    -------
    str (stream=False) or Iterator[str] (stream=True)
    """
    # Check if we need to fall back to another model
    if fallback:
        try:
            available_models = list_models(host)
            fallback_model = _select_fallback_model(model, available_models)
            
            if fallback_model:
                print(
                    f"Warning: Model '{model}' not available. "
                    f"Using fallback model '{fallback_model}' instead.",
                    file=sys.stderr
                )
                model = fallback_model
        except OllamaError:
            # If we can't list models, just proceed with the original model
            # and let the API call fail with a clear error message
            pass
    
    url = f"{host}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "options": {
            # Keep temperature low for deterministic code review
            "temperature": 0.2,
            "top_p": 0.9,
        },
    }

    if stream:
        return _stream_response(url, payload)
    else:
        return _blocking_response(url, payload)


def _blocking_response(url: str, payload: dict) -> str:
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["message"]["content"]
    except httpx.HTTPStatusError as exc:
        raise OllamaError(f"Ollama returned HTTP {exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        raise OllamaError(f"Cannot reach Ollama: {exc}") from exc
    except (KeyError, json.JSONDecodeError) as exc:
        raise OllamaError(f"Unexpected response format: {exc}") from exc


def _stream_response(url: str, payload: dict) -> Iterator[str]:
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            with client.stream("POST", url, json=payload) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if chunk.get("done"):
                        break
    except httpx.HTTPStatusError as exc:
        raise OllamaError(f"Ollama returned HTTP {exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        raise OllamaError(f"Cannot reach Ollama: {exc}") from exc
