from tests.test_agent import (
    test_agent_confirms_acceptable_offer,
    test_agent_records_events_when_gateway_is_available,
    test_agent_rejects_offer_when_counter_not_allowed,
    test_agent_requires_supplier_approval,
)
from tests.test_pipeline import (
    test_full_pipeline_with_backend_buyer_data,
    test_pipeline_calculates_distance_from_coordinates,
    test_pipeline_filters_buyer_outside_service_radius,
    test_pipeline_rejects_invalid_quantity,
    test_pipeline_returns_no_suitable_buyers,
)


TESTS = [
    test_full_pipeline_with_backend_buyer_data,
    test_pipeline_returns_no_suitable_buyers,
    test_pipeline_filters_buyer_outside_service_radius,
    test_pipeline_calculates_distance_from_coordinates,
    test_pipeline_rejects_invalid_quantity,
    test_agent_requires_supplier_approval,
    test_agent_confirms_acceptable_offer,
    test_agent_rejects_offer_when_counter_not_allowed,
    test_agent_records_events_when_gateway_is_available,
]


if __name__ == "__main__":
    for test in TESTS:
        test()
        print(f"PASS {test.__name__}")

    print(f"\n{len(TESTS)} tests passed.")
    
