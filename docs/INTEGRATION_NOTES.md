# Integration Notes

The backend now connects to the AI module through:

```text
app/services/ai_service.py
```

The matches API calls `find_ai_ranked_buyers()` instead of the older simple matching service. This keeps the database models unchanged while mapping backend rows into the AI contract.

## Current Bridge Assumptions

- `WasteListing.produce_type` maps to `waste_type`.
- Buyer coordinates are used to calculate distance.
- Buyer `max_capacity_kg` is used as both maximum quantity and current capacity.
- Buyer pickup is currently assumed available because the existing buyer model has no pickup field.
- Currency is currently set to `INR`.
- Accepted waste types are inferred from `buyer_type` until the backend adds a dedicated accepted-waste field.

## Recommended Backend Improvements

Add these fields to the buyer model when the team has time:

- `accepted_waste_types`
- `min_quantity_kg`
- `current_capacity_kg`
- `pickup_available`
- `service_radius_km`
- `availability_status`
- `currency`

