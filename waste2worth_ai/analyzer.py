import json
import os

from waste2worth_ai.knowledge_base import WASTE_KNOWLEDGE
from waste2worth_ai.schemas import WasteInput


def analyze_waste(waste_input: WasteInput, use_openai: bool = False):
    if use_openai:
        openai_result = _try_openai_analysis(waste_input)
        if openai_result:
            return openai_result

    return _rule_based_analysis(waste_input)


def _rule_based_analysis(waste_input: WasteInput):
    profile = WASTE_KNOWLEDGE.get(
        waste_input.waste_type,
        {
            "display_name": f"{waste_input.waste_type.title()} waste",
            "category": "Organic waste",
            "properties": ["biodegradable"],
            "suitable_uses": ["composting", "anaerobic_digestion"],
            "limitations": ["Waste composition should be verified before final routing."],
        },
    )

    limitations = list(profile["limitations"])
    if waste_input.condition in {"spoiled", "rotten", "contaminated"}:
        limitations.append("Condition may reduce suitability for some higher-value uses.")

    return {
        "waste_type": waste_input.waste_type,
        "display_name": profile["display_name"],
        "category": profile["category"],
        "quantity_kg": waste_input.quantity_kg,
        "condition": waste_input.condition,
        "location": waste_input.location,
        "available_from": waste_input.available_from,
        "available_until": waste_input.available_until,
        "properties": profile["properties"],
        "suitable_uses": profile["suitable_uses"],
        "limitations": limitations,
        "confidence": 0.84 if waste_input.waste_type in WASTE_KNOWLEDGE else 0.58,
        "source": "domain_rules",
    }


def _try_openai_analysis(waste_input: WasteInput):
    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI()
    schema = {
        "type": "json_schema",
        "name": "waste_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "waste_type": {"type": "string"},
                "display_name": {"type": "string"},
                "category": {"type": "string"},
                "quantity_kg": {"type": "number"},
                "condition": {"type": "string"},
                "location": {"type": "object", "additionalProperties": True},
                "properties": {"type": "array", "items": {"type": "string"}},
                "suitable_uses": {"type": "array", "items": {"type": "string"}},
                "limitations": {"type": "array", "items": {"type": "string"}},
                "confidence": {"type": "number"},
                "source": {"type": "string"},
            },
            "required": [
                "waste_type",
                "display_name",
                "category",
                "quantity_kg",
                "condition",
                "location",
                "properties",
                "suitable_uses",
                "limitations",
                "confidence",
                "source",
            ],
            "additionalProperties": False,
        },
    }

    response = client.responses.create(
        model=os.getenv("WASTE2WORTH_OPENAI_MODEL", "gpt-5-mini"),
        input=[
            {
                "role": "system",
                "content": "Analyze organic waste for resource recovery. Return only the requested JSON.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "waste_type": waste_input.waste_type,
                        "quantity_kg": waste_input.quantity_kg,
                        "condition": waste_input.condition,
                        "location": waste_input.location,
                        "notes": waste_input.notes,
                    }
                ),
            },
        ],
        text={"format": schema},
    )

    result = json.loads(response.output_text)
    result["source"] = "openai_responses_api"
    return result
