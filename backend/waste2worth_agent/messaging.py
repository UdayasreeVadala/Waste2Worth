"""AI-generated buyer outreach and negotiation.

The deterministic state machine decides *when* to act; the LLM decides *how* to
say it. Supplier rules (price floor, pickup requirement) are always enforced
deterministically on top of any LLM suggestion, so the agent can never
under-sell its own supplier.

For a hackathon demo without an API key, templated fallbacks produce
professional, locally-aware messages.
"""

from waste2worth_ai import llm

_MESSAGE_SCHEMA = {
    "properties": {
        "subject": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["subject", "body"],
}

_COUNTER_SCHEMA = {
    "properties": {
        "total_price": {"type": "number"},
        "pickup_included": {"type": "boolean"},
        "rationale": {"type": "string"},
    },
    "required": ["total_price", "pickup_included", "rationale"],
}


def _locale_hint(buyer):
    location = "".join(str(v) for v in (buyer.get("location") or {}).values()).lower()
    if any(token in location for token in ["india", "nashik", "mumbai", "pune", "delhi", "hyd"]):
        return "India (Hinglish-friendly, professional)"
    return "professional, neutral English"


def generate_outreach_message(waste_analysis, buyer, supplier_rules):
    """Return {subject, body, source}. The gateway decides delivery (email, etc.)."""
    location = buyer.get("location") or {}
    payload = {
        "waste": {
            "type": waste_analysis.get("display_name") or waste_analysis.get("waste_type"),
            "quantity_kg": waste_analysis.get("quantity_kg"),
            "condition": waste_analysis.get("condition"),
            "available_from": waste_analysis.get("available_from"),
            "available_until": waste_analysis.get("available_until"),
        },
        "buyer": {
            "name": buyer.get("name"),
            "business_type": buyer.get("business_type"),
            "location": location,
        },
        "supplier_rules": {
            "minimum_total_price": supplier_rules.get("minimum_total_price"),
            "requires_pickup": supplier_rules.get("requires_pickup"),
        },
        "locale_hint": _locale_hint(buyer),
    }

    llm_result = llm.chat_json(
        system_prompt=(
            "Write a concise, professional buyer outreach message for an organic waste recovery "
            "platform. The supplier has listed waste and approved this buyer. State what material, "
            "quantity and condition are available, mention the supplier's minimum acceptable total "
            "price and whether pickup is required. Keep it short and respectful. Respond with "
            "{subject, body}."
        ),
        user_payload=payload,
        name="buyer_outreach_message",
        schema=_MESSAGE_SCHEMA,
    )
    if llm_result:
        return {
            "subject": llm_result.get("subject", ""),
            "body": llm_result.get("body", ""),
            "source": "openai_messaging",
        }

    return _template_message(waste_analysis, buyer, supplier_rules)


def _template_message(waste_analysis, buyer, supplier_rules):
    waste_label = waste_analysis.get("display_name") or waste_analysis.get("waste_type", "organic waste")
    subject = (
        f"Available organic feedstock: {waste_label} "
        f"({waste_analysis.get('quantity_kg')} kg)"
    )
    body = (
        f"Hello {buyer.get('name')},\n\n"
        f"We have {waste_analysis.get('quantity_kg')} kg of {waste_label.lower()} "
        f"({'condition: ' + waste_analysis.get('condition') if waste_analysis.get('condition') else 'condition varies'}) "
        f"available for recovery.\n"
        f"Minimum acceptable total price: {supplier_rules.get('minimum_total_price')}\n"
        f"Pickup required: {'yes' if supplier_rules.get('requires_pickup') else 'no'}\n\n"
        f"Would your facility be able to accept this feedstock? "
        f"Please reply with your best offer.\n\nBest regards,\nWaste2Worth"
    )
    return {"subject": subject, "body": body, "source": "template"}


def suggest_counter_offer(waste_analysis, buyer, supplier_rules, latest_offer=None):
    """Propose a counter offer. The result is clamped by the deterministic floor
    so the LLM can negotiate up, never down below the supplier's minimum.
    """
    floor = supplier_rules.get("minimum_total_price", 0)
    pickup = supplier_rules.get("requires_pickup", True)

    payload = {
        "waste_type": waste_analysis.get("display_name") or waste_analysis.get("waste_type"),
        "quantity_kg": waste_analysis.get("quantity_kg"),
        "buyer_name": buyer.get("name"),
        "buyer_offer": latest_offer,
        "supplier_minimum_total_price": floor,
        "requires_pickup": pickup,
        "locale_hint": _locale_hint(buyer),
    }

    llm_result = llm.chat_json(
        system_prompt=(
            "You are a negotiation assistant for a waste-supplier. The buyer's latest offer is "
            "below the supplier's minimum total price. Propose a counter offer: a total price at or "
            "above the supplier minimum (never below), and whether pickup should be included. "
            "Give a one-line rationale. Respond with {total_price, pickup_included, rationale}."
        ),
        user_payload=payload,
        name="counter_offer_suggestion",
        schema=_COUNTER_SCHEMA,
    )

    if llm_result:
        try:
            total_price = max(float(llm_result["total_price"]), floor)
        except (KeyError, TypeError, ValueError):
            total_price = floor
        return {
            "total_price": round(total_price, 2),
            "pickup_included": bool(llm_result.get("pickup_included", pickup)),
            "rationale": llm_result.get("rationale") or "Meeting the supplier's minimum acceptable price.",
            "source": "openai_negotiation",
        }

    return {
        "total_price": floor,
        "pickup_included": pickup,
        "rationale": "Countering at the supplier's minimum acceptable total price.",
        "source": "rule_negotiation",
    }
