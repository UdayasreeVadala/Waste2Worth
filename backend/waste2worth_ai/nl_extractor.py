"""Turn plain-English waste descriptions into a structured listing.

This is the "no technical classifications needed" promise made real: a farmer
writes "I have around 700 kg of spoiled tomatoes from my farm in Nashik" and the
system extracts the structured fields itself. LLM extraction is preferred; a
rule-based extractor guarantees the flow works with zero API keys.
"""

import re

from waste2worth_ai import llm

WASTE_TYPE_KEYWORDS = {
    "tomato": ["tomato", "tomatoes"],
    "onion": ["onion", "onions"],
    "potato": ["potato", "potatoes", "aloo"],
    "banana": ["banana", "bananas"],
    "mango": ["mango", "mangoes", "mangos", "aam"],
    "citrus": ["citrus", "orange", "lemon", "lime", "mosambi", "santra"],
    "crop": ["crop residue", "crop", "stubble", "straw", "husk", "parali", "sugarcane", "bagasse"],
    "grain": ["grain", "grains", "wheat", "rice", "paddy", "bajra", "jowar", "maize", "corn"],
    "vegetable": ["vegetable", "vegetables", "sabzi", "veggies"],
    "fruit": ["fruit", "fruits"],
    "food": ["food", "food waste", "kitchen waste", "leftover"],
    "organic": ["organic", "biodegradable", "compostable"],
}

CONDITION_KEYWORDS = {
    "spoiled": ["spoiled", "spoilt", "rotten", "bad", "expired", "wasted", "overripe", "damaged", "kharab"],
    "fresh": ["fresh", "new"],
    "mixed": ["mixed", "assorted"],
    "processed": ["processed", "peel", "peels", "pulp", "seed"],
}

_QUANTITY_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:kg|kgs|kilograms?|tonne?s?|tons?|quintals?|t|tonnes?)\b",
    re.IGNORECASE,
)
_LOCATION_RE = re.compile(
    r"\b(?:in|near|from|around)\s+([A-Za-z][A-Za-z\s,.-]{1,40})\b"
)


def _rule_based_extraction(text):
    lowered = text.lower()

    waste_type = None
    for key, keywords in WASTE_TYPE_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            waste_type = key
            break
    if waste_type is None:
        waste_type = "organic"

    quantity_kg = None
    for match in _QUANTITY_RE.finditer(text):
        number = float(match.group(1))
        unit = match.group(0).lower()
        if "ton" in unit:
            number *= 1000
        elif "quintal" in unit:
            number *= 100
        quantity_kg = number
        break

    condition = "unknown"
    for key, keywords in CONDITION_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            condition = key
            break

    location = None
    location_match = _LOCATION_RE.search(text)
    if location_match:
        candidate = location_match.group(1).strip().rstrip(",.; ")
        for stop in (
            " available", " next", " this", " tomorrow", " today", " from my",
            " in my", " at my", " on my", " for sale", " if",
        ):
            cut = candidate.lower().find(stop)
            if cut != -1:
                candidate = candidate[:cut].rstrip(" ,;")
                break
        for splitter in (" in ", " at ", " near ", " around ", " from "):
            lowered = candidate.lower()
            idx = lowered.rfind(splitter)
            if idx != -1:
                candidate = candidate[idx + len(splitter):].strip(" ,;")
        if candidate and len(candidate) > 2 and len(candidate) < 40:
            location = candidate

    confidence = 0.5
    if waste_type in WASTE_TYPE_KEYWORDS and quantity_kg is not None:
        confidence = 0.75

    return {
        "waste_type": waste_type,
        "quantity_kg": quantity_kg,
        "condition": condition,
        "location": location,
        "notes": text,
        "source": "nl_rules",
        "confidence": confidence,
    }


_SCHEMA = {
    "properties": {
        "waste_type": {"type": "string"},
        "quantity_kg": {"type": "number"},
        "condition": {"type": "string"},
        "location": {"type": "string"},
        "notes": {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": ["waste_type", "quantity_kg", "condition", "location", "notes", "confidence"],
}


def extract_waste_from_text(text):
    """Extract a structured listing from free text. Returns a dict or None."""
    if not text or not text.strip():
        return None

    text = text.strip()

    llm_result = llm.chat_json(
        system_prompt=(
            "Extract structured organic waste listing details from a free-text description. "
            "waste_type must be one of: tomato, onion, potato, banana, mango, citrus, grain, "
            "vegetable, fruit, crop, food, organic, other. quantity_kg is the amount in kilograms. "
            "condition is one of: fresh, spoiled, mixed, processed, unknown. "
            "location is the city or region name if mentioned, else empty string. "
            "Set confidence 0-1 reflecting how certain you are of the quantity."
        ),
        user_payload={"description": text},
        name="waste_listing_extraction",
        schema=_SCHEMA,
    )
    if llm_result:
        result = dict(llm_result)
        result["notes"] = text
        result["source"] = "openai_nl_extraction"
        return result

    return _rule_based_extraction(text)
