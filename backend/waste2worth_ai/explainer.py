"""Plain-language explanation of buyer rankings.

Rankings are deterministic, but a deterministic score is not a story. This module
turns the factor breakdown into a human explanation — LLM-written when
available, rule-based otherwise.
"""

from waste2worth_ai import llm

_SCHEMA = {
    "properties": {
        "summary": {"type": "string"},
        "buyer_reasons": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "buyer_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["buyer_id", "reason"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["summary", "buyer_reasons"],
}


def explain_ranking(waste_analysis, ranked_buyers):
    """Return {summary, buyer_reasons} for a ranked buyer list."""
    if not ranked_buyers:
        return {"summary": "No suitable buyer currently matches this waste.", "buyer_reasons": []}

    buyer_rows = [
        {
            "buyer_id": row["buyer_id"],
            "name": row["name"],
            "business_type": row["business_type"],
            "distance_km": row["distance_km"],
            "price_per_kg": row["price_per_kg"],
            "currency": row["currency"],
            "pickup_available": row["pickup_available"],
            "estimated_margin": row["estimated_margin"],
            "score": row["score"],
            "factor_breakdown": row["factor_breakdown"],
        }
        for row in ranked_buyers
    ]

    llm_result = llm.chat_json(
        system_prompt=(
            "Explain, in plain language a non-technical supplier can understand, why each buyer "
            "was ranked where it was for this organic waste opportunity. Weigh earnings, distance, "
            "pickup availability, capacity and availability. Be concrete and honest about trade-offs "
            "(for example when a closer buyer with pickup beats a slightly higher price). "
            "Do not invent facts that are not in the data."
        ),
        user_payload={
            "waste": {
                "type": waste_analysis["display_name"],
                "quantity_kg": waste_analysis["quantity_kg"],
                "condition": waste_analysis["condition"],
            },
            "ranked_buyers": buyer_rows,
        },
        name="ranking_explanation",
        schema=_SCHEMA,
    )
    if llm_result and llm_result.get("buyer_reasons"):
        reasons = {r["buyer_id"]: r["reason"] for r in llm_result["buyer_reasons"]}
        return {
            "summary": llm_result.get("summary") or _fallback_summary(waste_analysis, ranked_buyers),
            "buyer_reasons": [
                {"buyer_id": row["buyer_id"], "reason": reasons.get(row["buyer_id"], row["explanation"])}
                for row in ranked_buyers
            ],
            "source": "openai_explanation",
        }

    return {
        "summary": _fallback_summary(waste_analysis, ranked_buyers),
        "buyer_reasons": [
            {"buyer_id": row["buyer_id"], "reason": row["explanation"]} for row in ranked_buyers
        ],
        "source": "factor_rules",
    }


def _fallback_summary(waste_analysis, ranked_buyers):
    top = ranked_buyers[0]
    margin = top["estimated_margin"]
    return (
        f"{top['name']} is the top match for your {waste_analysis['display_name'].lower()} because "
        f"it offers the best balance of net earning ({margin['currency']} "
        f"{margin['estimated_supplier_earnings']}), distance ({top['distance_km']} km) and service. "
        f"{len(ranked_buyers)} suitable buyer(s) were found."
    )
