import os

# Hermetic test runs: never make real LLM calls during the test suite.
os.environ.setdefault("WASTE2WORTH_USE_AI", "0")

from tests.test_agent import (
    test_agent_confirms_acceptable_offer,
    test_agent_records_events_when_gateway_is_available,
    test_agent_rejects_offer_when_counter_not_allowed,
    test_agent_requires_supplier_approval,
)
from tests.test_extractors import (
    test_data_uri_encoding,
    test_nl_extraction_crop_residue_beats_grain,
    test_nl_extraction_city_after_in,
    test_nl_extraction_disabled_ai_still_extracts,
    test_nl_extraction_returns_none_on_empty,
    test_nl_extraction_rule_based_kg,
    test_nl_extraction_rule_based_quantity_tonnes,
    test_nl_extraction_rule_based_quintal,
    test_vision_returns_none_without_key,
    test_vision_returns_none_when_disabled,
)
from tests.test_impact import (
    test_impact_embeds_economic_and_factors,
    test_impact_methane_and_co2e_math,
    test_impact_route_co_benefits,
    test_impact_summary_aggregates,
)
from tests.test_messaging import (
    test_counter_offer_floor_enforced,
    test_counter_offer_zero_floor,
    test_outreach_template_contains_key_facts,
)
from tests.test_pipeline import (
    test_full_pipeline_with_backend_buyer_data,
    test_pipeline_calculates_distance_from_coordinates,
    test_pipeline_filters_buyer_outside_service_radius,
    test_pipeline_rejects_invalid_quantity,
    test_pipeline_returns_no_suitable_buyers,
    test_pipeline_reports_impact_and_explanation,
)
from tests.test_scoring import (
    test_pickup_bonus_and_breakdown_consistent,
    test_ranked_buyers_have_factor_breakdown,
    test_scoring_config_version_present,
)


TESTS = [
    test_full_pipeline_with_backend_buyer_data,
    test_pipeline_returns_no_suitable_buyers,
    test_pipeline_filters_buyer_outside_service_radius,
    test_pipeline_calculates_distance_from_coordinates,
    test_pipeline_rejects_invalid_quantity,
    test_pipeline_reports_impact_and_explanation,
    test_agent_requires_supplier_approval,
    test_agent_confirms_acceptable_offer,
    test_agent_rejects_offer_when_counter_not_allowed,
    test_agent_records_events_when_gateway_is_available,
    test_impact_methane_and_co2e_math,
    test_impact_route_co_benefits,
    test_impact_embeds_economic_and_factors,
    test_impact_summary_aggregates,
    test_nl_extraction_rule_based_quantity_tonnes,
    test_nl_extraction_rule_based_kg,
    test_nl_extraction_rule_based_quintal,
    test_nl_extraction_crop_residue_beats_grain,
    test_nl_extraction_city_after_in,
    test_nl_extraction_returns_none_on_empty,
    test_nl_extraction_disabled_ai_still_extracts,
    test_data_uri_encoding,
    test_vision_returns_none_without_key,
    test_vision_returns_none_when_disabled,
    test_outreach_template_contains_key_facts,
    test_counter_offer_floor_enforced,
    test_counter_offer_zero_floor,
    test_ranked_buyers_have_factor_breakdown,
    test_pickup_bonus_and_breakdown_consistent,
    test_scoring_config_version_present,
]


if __name__ == "__main__":
    for test in TESTS:
        test()
        print(f"PASS {test.__name__}")

    print(f"\n{len(TESTS)} tests passed.")
