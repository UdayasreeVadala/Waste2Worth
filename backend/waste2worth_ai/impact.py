"""Environmental and economic impact estimation for a waste opportunity.

The engine answers the question a judge or investor would ask first:
"if this platform actually works, what does it *do* for the planet and for the
people involved?" Every quantity is derived from named factors in
`impact_factors.py` so the methodology is auditable.
"""

from waste2worth_ai import impact_factors as F


def _route_co_benefit(route):
    """Recovery co-benefit per kg, over and above avoided landfill methane."""
    if route == "anaerobic_digestion":
        return {
            "label": "Biogas displacing grid electricity",
            "detail": "Electricity generated from recovered biogas offsets grid power.",
            "kg_co2e_per_kg": F.AD_ELECTRICAL_KWH_PER_KG * F.GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH,
        }
    if route == "composting":
        return {
            "label": "Fertiliser offset and soil carbon",
            "detail": "Compost replaces synthetic fertiliser and returns carbon to soil.",
            "kg_co2e_per_kg": F.COMPOST_CO_BENEFIT_KG_CO2E_PER_KG,
        }
    if route == "vermicomposting":
        return {
            "label": "Fertiliser offset and soil carbon",
            "detail": "Vermicompost replaces synthetic fertiliser and returns carbon to soil.",
            "kg_co2e_per_kg": F.COMPOST_CO_BENEFIT_KG_CO2E_PER_KG,
        }
    if route == "biochar":
        return {
            "label": "Long-lived carbon storage",
            "detail": "Stable biochar carbon sequestered in soil for centuries.",
            "kg_co2e_per_kg": (
                F.BIOCHAR_DRY_MATTER_FRACTION
                * F.BIOCHAR_CARBON_FRACTION
                * F.BIOCHAR_STABLE_RETENTION
                * F.CO2_PER_CARBON
            ),
        }
    return None


def estimate_impact(waste_analysis, route=None, economic=None):
    """Estimate the environmental and economic impact of one listing.

    Args:
        waste_analysis: dict from `analyzer.analyze_waste` (or compatible).
        route: recommended processing route id (e.g. "anaerobic_digestion").
        economic: optional margin dict from pricing (`estimate_margin` output).
    """
    quantity_kg = float(waste_analysis["quantity_kg"])

    methane_kg = round(quantity_kg * F.METHANE_YIELD_PER_KG, 3)
    co2e_gwp100 = round(methane_kg * F.GWP_CH4_100, 3)
    co2e_gwp20 = round(methane_kg * F.GWP_CH4_20, 3)

    co_benefit = None
    if route:
        factor = _route_co_benefit(route)
        if factor:
            co_benefit = {
                "label": factor["label"],
                "detail": factor["detail"],
                "kg_co2e": round(quantity_kg * factor["kg_co2e_per_kg"], 3),
            }

    result = {
        "quantity_kg": quantity_kg,
        "route": route,
        "methane_avoided_kg": methane_kg,
        "co2e_avoided_kg_gwp100": co2e_gwp100,
        "co2e_avoided_kg_gwp20": co2e_gwp20,
        "landfill_diverted_kg": quantity_kg,
        "co_benefit": co_benefit,
        "equivalencies": {
            "km_driven_equivalent": round(co2e_gwp100 / F.KG_CO2E_PER_KM_DRIVEN),
            "coal_kwh_equivalent": round(co2e_gwp100 / F.KG_CO2E_PER_KWH_COAL),
            "tree_years_equivalent": round(co2e_gwp100 / F.KG_CO2E_PER_TREE_YEAR, 1),
        },
        "factors": {
            "version": F.FACTOR_VERSION,
            "methane_yield_per_kg": F.METHANE_YIELD_PER_KG,
            "gwp_ch4_100": F.GWP_CH4_100,
            "gwp_ch4_20": F.GWP_CH4_20,
        },
    }

    if economic:
        result["economic"] = economic

    return result


def impact_summary(rows):
    """Aggregate a list of per-listing impact estimates into a dashboard summary."""
    total_quantity_kg = sum(float(r.get("quantity_kg") or 0) for r in rows)
    total_methane_kg = sum(float(r.get("methane_avoided_kg") or 0) for r in rows)
    total_co2e_100 = sum(float(r.get("co2e_avoided_kg_gwp100") or 0) for r in rows)
    total_co2e_20 = sum(float(r.get("co2e_avoided_kg_gwp20") or 0) for r in rows)
    total_co_benefit = sum(float((r.get("co_benefit") or {}).get("kg_co2e") or 0) for r in rows)
    total_supplier_earnings = sum(
        float((r.get("economic") or {}).get("estimated_supplier_earnings") or 0) for r in rows
    )
    total_buyer_offer = sum(float((r.get("economic") or {}).get("buyer_offer") or 0) for r in rows)

    return {
        "listings_count": len(rows),
        "total_quantity_kg": round(total_quantity_kg, 2),
        "total_methane_avoided_kg": round(total_methane_kg, 2),
        "total_co2e_avoided_kg_gwp100": round(total_co2e_100, 2),
        "total_co2e_avoided_kg_gwp20": round(total_co2e_20, 2),
        "total_co_benefit_kg_co2e": round(total_co_benefit, 2),
        "total_buyer_offer": round(total_buyer_offer, 2),
        "total_supplier_earnings": round(total_supplier_earnings, 2),
        "equivalencies": {
            "km_driven_equivalent": round(total_co2e_100 / F.KG_CO2E_PER_KM_DRIVEN),
            "coal_kwh_equivalent": round(total_co2e_100 / F.KG_CO2E_PER_KWH_COAL),
            "tree_years_equivalent": round(total_co2e_100 / F.KG_CO2E_PER_TREE_YEAR, 1),
        },
        "factors": {"version": F.FACTOR_VERSION},
    }
