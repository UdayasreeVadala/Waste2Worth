# Agent Contract

The agent must never contact a buyer before supplier approval.

## Required Integrations

The backend must provide:

- `BuyerCommunicationGateway`
- `TransactionGateway`
- `EventGateway` optional, recommended for live activity logs

This keeps the agent real. Email, WhatsApp, SMS, or in-app messaging can be plugged in later without rewriting the workflow.

## Agent Method

```python
agent.contact_and_negotiate(
    transaction_id="txn_123",
    waste_analysis=analysis,
    selected_buyer=best_buyer,
    supplier_rules={
        "minimum_total_price": 180,
        "requires_pickup": true,
        "allow_counter_offer": true
    },
    supplier_approved_contact=true,
)
```

## Event Format

```json
{
  "transaction_id": "txn_123",
  "event_type": "buyer_contacted",
  "actor": "ai_agent",
  "message": "Buyer contacted.",
  "payload": {},
  "created_at": "2026-08-09T10:05:00+05:30"
}
```

## Status Values

Use lowercase snake_case:

```text
waiting_for_supplier_approval
buyer_contacted
offer_received
counter_offer_sent
deal_confirmed
offer_rejected
```
