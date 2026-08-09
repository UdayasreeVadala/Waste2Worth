# Waste2Worth AI + Agent Module

This is the production-shaped AI and agent module for the Waste2Worth project.

It does not own frontend, backend, authentication, database, or project startup. The backend calls this module with real supplier waste input and real buyer data.

## Responsibilities

- Analyze supplier waste into a structured profile
- Recommend the best practical processing route
- Rank real buyers from backend/database data
- Estimate supplier earnings after transport and platform fee
- Run supplier-approved agent workflow
- Enforce supplier negotiation rules

## Backend Entry Point: AI

Use:

```python
from waste2worth_ai.pipeline import evaluate_waste_opportunity

result = evaluate_waste_opportunity(
    waste_input={
        "waste_type": "tomato",
        "quantity_kg": 700,
        "condition": "spoiled",
        "location": {"city": "Nashik", "country": "India"},
    },
    buyers=[...real buyer rows from backend...],
)
```

The module returns:

- `analysis`
- `recommended_use`
- `ranked_buyers`
- `best_buyer`
- `requires_supplier_approval`
- `agent_status`
- `error`

## Backend Entry Point: Agent

Use:

```python
from waste2worth_agent import Waste2WorthAgent

agent = Waste2WorthAgent(
    communication_gateway=your_communication_gateway,
    transaction_gateway=your_transaction_gateway,
    event_gateway=your_event_gateway,
)

result = agent.contact_and_negotiate(
    transaction_id="txn_123",
    waste_analysis=analysis,
    selected_buyer=best_buyer,
    supplier_rules={
        "minimum_total_price": 180,
        "requires_pickup": True,
        "allow_counter_offer": True,
    },
    supplier_approved_contact=True,
)
```

## Real-Time Rules

- Backend must send live buyer records into the AI pipeline.
- The agent never contacts a buyer before supplier approval.
- Internal statuses use lowercase snake_case.
- `distance_km` is required unless both supplier and buyer locations include coordinates.
- If no buyer matches, the AI returns `NO_SUITABLE_BUYERS` instead of guessing.
- No external package is required for the default rule-based pipeline.

## Optional OpenAI Use

If `OPENAI_API_KEY` is available and the `openai` package is installed, the analyzer can use the OpenAI Responses API for richer structured analysis. If not, it uses the local domain rules so the backend still works.

The official OpenAI documentation recommends storing the API key in `OPENAI_API_KEY`, and the SDK reads it from the environment.

## Run Tests

```bash
python run_tests.py
```

Current coverage:

- valid full pipeline
- no suitable buyers
- buyer outside service radius
- coordinate distance calculation
- invalid quantity rejection
- supplier approval guard
- successful deal confirmation
- rejected offer when counter is disabled
- event logging
