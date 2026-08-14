from waste2worth_ai.impact import estimate_impact, impact_summary
from waste2worth_ai import impact_factors as F


def test_impact_methane_and_co2e_math():
    analysis = {"quantity_kg": 1000, "waste_type": "tomato", "display_name": "Tomato waste"}
    impact = estimate_impact(analysis, route="anaerobic_digestion")

    assert impact["methane_avoided_kg"] == round(1000 * F.METHANE_YIELD_PER_KG, 3)
    assert impact["co2e_avoided_kg_gwp100"] == round(
        1000 * F.METHANE_YIELD_PER_KG * F.GWP_CH4_100, 3
    )
    assert impact["co2e_avoided_kg_gwp20"] > impact["co2e_avoided_kg_gwp100"]
    assert impact["landfill_diverted_kg"] == 1000
    assert impact["equivalencies"]["km_driven_equivalent"] > 0


def test_impact_route_co_benefits():
    analysis = {"quantity_kg": 100, "waste_type": "tomato", "display_name": "Tomato waste"}
    ad = estimate_impact(analysis, route="anaerobic_digestion")
    biochar = estimate_impact(analysis, route="biochar")
    plain = estimate_impact(analysis, route=None)

    assert ad["co_benefit"] is not None
    assert ad["co_benefit"]["label"] == "Biogas displacing grid electricity"
    assert biochar["co_benefit"]["label"] == "Long-lived carbon storage"
    assert plain["co_benefit"] is None


def test_impact_embeds_economic_and_factors():
    analysis = {"quantity_kg": 700, "waste_type": "tomato", "display_name": "Tomato waste"}
    economic = {
        "currency": "INR",
        "buyer_offer": 21000,
        "transport_cost": 0,
        "platform_fee": 630,
        "estimated_supplier_earnings": 20370,
    }
    impact = estimate_impact(analysis, route="composting", economic=economic)

    assert impact["economic"]["estimated_supplier_earnings"] == 20370
    assert impact["factors"]["version"] == F.FACTOR_VERSION


def test_impact_summary_aggregates():
    rows = [
        estimate_impact({"quantity_kg": 100, "waste_type": "tomato", "display_name": "Tomato waste"}, route="composting"),
        estimate_impact({"quantity_kg": 200, "waste_type": "onion", "display_name": "Onion waste"}, route="anaerobic_digestion"),
    ]
    summary = impact_summary(rows)

    assert summary["listings_count"] == 2
    assert summary["total_quantity_kg"] == 300
    assert summary["total_co2e_avoided_kg_gwp100"] > 0
    assert summary["equivalencies"]["tree_years_equivalent"] > 0
