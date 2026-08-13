# AI API Contract

## Evaluate Waste Opportunity

Backend calls:

```python
evaluate_waste_opportunity(waste_input, buyers, use_openai=False)
```

### Waste Input

```json
{
  "waste_type": "tomato",
  "quantity_kg": 700,
  "condition": "spoiled",
  "available_from": "2026-08-09T10:00:00+05:30",
  "available_until": "2026-08-09T18:00:00+05:30",
  "location": {
    "city": "Nashik",
    "country": "India"
  },
  "photo_url": null,
  "notes": null
}
```

### Buyer Input

```json
{
  "id": "buyer_123",
  "name": "GreenBio Energy",
  "business_type": "Biogas plant",
  "location": {
    "city": "Nashik",
    "country": "India"
  },
  "distance_km": 25,
  "service_radius_km": 50,
  "accepted_waste": ["tomato", "vegetable"],
  "min_quantity_kg": 300,
  "max_quantity_kg": 3000,
  "current_capacity_kg": 1500,
  "price_per_kg": 0.30,
  "currency": "USD",
  "pickup_available": true,
  "availability_status": "available"
}
```

If `distance_km` is not provided, both locations must include `latitude` and `longitude` so the AI module can calculate distance.

### Output

```json
{
  "analysis": {},
  "recommended_use": {},
  "ranked_buyers": [],
  "best_buyer": {},
  "requires_supplier_approval": true,
  "agent_status": "waiting_for_supplier_approval"
}
```

If no buyers match:

```json
{
  "best_buyer": null,
  "agent_status": "no_suitable_buyers",
  "error": {
    "code": "NO_SUITABLE_BUYERS",
    "message": "No buyer currently matches this waste listing."
  }
}
```

Internal statuses must use lowercase snake_case.
