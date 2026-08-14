from waste2worth_ai.analyzer import analyze_waste
from waste2worth_ai.explainer import explain_ranking
from waste2worth_ai.impact import estimate_impact
from waste2worth_ai.matcher import rank_buyers
from waste2worth_ai.recommender import recommend_processing_route
from waste2worth_ai.validation import parse_buyer, parse_waste_input, resolve_buyer_distances


def evaluate_waste_opportunity(waste_input, buyers, use_openai=False):
    parsed_waste = parse_waste_input(waste_input)
    parsed_buyers = resolve_buyer_distances(parsed_waste, [parse_buyer(buyer) for buyer in buyers])

    analysis = analyze_waste(parsed_waste, use_openai=use_openai)
    recommendation = recommend_processing_route(analysis, parsed_buyers)
    ranked_buyers = rank_buyers(analysis, parsed_buyers)

    best_buyer = ranked_buyers[0] if ranked_buyers else None
    economic = best_buyer["estimated_margin"] if best_buyer else None
    impact = estimate_impact(analysis, route=recommendation["recommended_route"], economic=economic)
    explanation = explain_ranking(analysis, ranked_buyers)

    return {
        "analysis": analysis,
        "recommended_use": recommendation,
        "ranked_buyers": ranked_buyers,
        "best_buyer": best_buyer,
        "impact": impact,
        "explanation": explanation,
        "requires_supplier_approval": True,
        "agent_status": "waiting_for_supplier_approval" if ranked_buyers else "no_suitable_buyers",
        "error": None
        if ranked_buyers
        else {
            "code": "NO_SUITABLE_BUYERS",
            "message": "No buyer currently matches this waste listing.",
        },
    }
