"""Centralised, optional OpenAI access for the AI layer.

Every AI capability follows the same pattern:
    - if AI is disabled or the API key is missing -> return None (caller falls back)
    - if the model call fails -> return None (caller falls back)

This makes the whole system run with zero external dependencies (rule-based),
and transparently upgrades to LLM intelligence when configured. The `source`
field on every result lets consumers tell which path produced it — honesty by
construction.
"""

import json
import os

ENV_FLAG = "WASTE2WORTH_USE_AI"
ENV_MODEL = "WASTE2WORTH_OPENAI_MODEL"
ENV_VISION_MODEL = "WASTE2WORTH_VISION_MODEL"

DEFAULT_MODEL = "gpt-5-mini"
DEFAULT_VISION_MODEL = "gpt-5-mini"


def ai_enabled():
    return os.getenv(ENV_FLAG, "1").strip().lower() not in {"0", "false", "no", "off"}


def has_api_key():
    return bool(os.getenv("OPENAI_API_KEY"))


def _client():
    if not has_api_key():
        return None
    try:
        from openai import OpenAI
    except ImportError:
        return None
    return OpenAI()


def _schema(name, properties, required):
    return {
        "type": "json_schema",
        "name": name,
        "strict": True,
        "schema": {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        },
    }


def chat_json(system_prompt, user_payload, name, schema, model=None):
    """Call the model with strict JSON output. Returns a dict or None."""
    if not ai_enabled():
        return None

    client = _client()
    if client is None:
        return None

    try:
        response = client.responses.create(
            model=model or os.getenv(ENV_MODEL, DEFAULT_MODEL),
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload)},
            ],
            text={"format": _schema(name, schema["properties"], schema["required"])},
        )
        return json.loads(response.output_text)
    except Exception:
        return None


def chat_vision(user_prompt, image_source, name, schema, model=None):
    """Ask the model to inspect an image. `image_source` is a URL or a data URI.
    Returns a dict or None.
    """
    if not ai_enabled():
        return None

    client = _client()
    if client is None:
        return None

    if image_source.startswith(("http://", "https://", "data:")):
        image_part = {"type": "input_image", "image_url": {"url": image_source}}
    else:
        image_part = {"type": "input_image", "image_url": {"url": f"data:image/jpeg;base64,{image_source}"}}

    try:
        response = client.responses.create(
            model=model or os.getenv(ENV_VISION_MODEL, DEFAULT_VISION_MODEL),
            input=[
                {"role": "system", "content": user_prompt},
                {"role": "user", "content": [{"type": "input_text", "text": user_prompt}, image_part]},
            ],
            text={"format": _schema(name, schema["properties"], schema["required"])},
        )
        return json.loads(response.output_text)
    except Exception:
        return None
