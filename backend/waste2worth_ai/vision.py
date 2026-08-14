"""Image-based waste classification.

A photo of a pile of tomatoes is worth a thousand dropdowns. When a photo is
uploaded, a vision model identifies the waste type, condition and an estimated
quantity; with no API key configured the call returns None and the caller keeps
whatever structured data it already has.
"""

import base64

from waste2worth_ai import llm


def build_data_uri(raw_bytes, mime_type="image/jpeg"):
    return f"data:{mime_type};base64,{base64.b64encode(raw_bytes).decode('ascii')}"


def _schema():
    return {
        "properties": {
            "waste_type": {"type": "string"},
            "condition": {"type": "string"},
            "estimated_quantity_kg": {"type": "number"},
            "confidence": {"type": "number"},
            "notes": {"type": "string"},
        },
        "required": [
            "waste_type",
            "condition",
            "estimated_quantity_kg",
            "confidence",
            "notes",
        ],
    }


def classify_waste_image(image_source):
    """Classify a waste photo. `image_source` is an http(s) URL, a data URI, or
    a raw base64 string. Returns a dict or None.
    """
    if not image_source:
        return None

    result = llm.chat_vision(
        user_prompt=(
            "This photo shows organic waste. Identify the dominant waste type from: "
            "tomato, onion, potato, banana, mango, citrus, grain, vegetable, fruit, "
            "crop, food, organic, other. Estimate the condition (fresh, spoiled, mixed, "
            "processed, unknown) and an approximate quantity in kilograms based on visible "
            "volume. Add brief notes and a confidence 0-1 for the type identification. "
            "Return only the requested JSON."
        ),
        image_source=image_source,
        name="waste_image_classification",
        schema=_schema(),
    )
    if result:
        result["source"] = "openai_vision"
        return result
    return None
