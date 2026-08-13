# Integration Notes

The backend now connects to the AI module through:

```text
app/services/ai_service.py
```

The matches API calls `find_ai_ranked_buyers()` instead of the older simple matching service. This maps backend rows into the AI contract without forcing the frontend to know AI internals.

## Current Bridge Assumptions

- `WasteListing.produce_type` maps to `waste_type`.
- Buyer coordinates are used to calculate distance.
- Buyer coordinates are used to calculate distance when `distance_km` is not supplied directly.
- `current_capacity_kg` falls back to `max_capacity_kg` when empty.
- `accepted_waste_types` is stored as a comma-separated string for the MVP.
- Agent events are returned by the route but are not persisted in a dedicated events table yet.

## Added Buyer Fields

The buyer model now supports:

- `accepted_waste_types`
- `min_quantity_kg`
- `current_capacity_kg`
- `pickup_available`
- `service_radius_km`
- `availability_status`
- `currency`

## Recommended Next Backend Improvement

Add a dedicated `transaction_events` table when the team wants persistent agent activity logs.
