from waste2worth_ai.knowledge_base import PROCESSING_ROUTES


def recommend_processing_route(waste_analysis, buyers):
    scores = {route: 0.0 for route in waste_analysis["suitable_uses"]}

    for route in scores:
        route_info = PROCESSING_ROUTES.get(route, {})
        fit_properties = route_info.get("fit_properties", [])
        scores[route] += 10 * len(set(waste_analysis["properties"]) & set(fit_properties))

        for buyer in buyers:
            business_type = buyer.business_type.lower()
            if any(keyword in business_type for keyword in route_info.get("buyer_keywords", [])):
                scores[route] += 12
                if buyer.pickup_available:
                    scores[route] += 4
                scores[route] += min(buyer.current_capacity_kg / max(waste_analysis["quantity_kg"], 1), 3)

    best_route = max(scores, key=scores.get)
    label = PROCESSING_ROUTES.get(best_route, {}).get("label", best_route.replace("_", " ").title())

    return {
        "recommended_route": best_route,
        "recommended_label": label,
        "route_scores": {key: round(value, 2) for key, value in scores.items()},
        "reason": _reason(label, waste_analysis, buyers),
    }


def _reason(label, waste_analysis, buyers):
    matching_buyers = len([buyer for buyer in buyers if buyer.availability_status == "available"])
    return (
        f"{label} is the strongest route for {waste_analysis['display_name']} based on material fit, "
        f"available buyer demand, capacity, pickup feasibility, and estimated economics across "
        f"{matching_buyers} available buyer records."
    )

