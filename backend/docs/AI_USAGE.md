# AI Usage — What Is AI, What Is Rules, and Why

This project is deliberately **honest by construction**: every AI capability has a
`source` field in its output so consumers and judges can see exactly which engine
produced a result. The system runs fully with zero external dependencies and
upgrades to LLM intelligence when an `OPENAI_API_KEY` with quota is configured
(`WASTE2WORTH_USE_AI=1`, the default).

## Capabilities

| Capability | LLM engine | Rule engine | Why both |
|---|---|---|---|
| **Waste analysis** (`analyzer.py`) | Classifies waste type/properties/uses via the Responses API (structured JSON) | Domain knowledge base (`knowledge_base.py`, 13 waste types + 4 routes) | Rules are instant and free; the LLM adds nuance for unusual materials |
| **Natural-language listing** (`nl_extractor.py`) | Extracts type / quantity / condition / location from plain English ("around 700 kg of spoiled tomatoes near Nashik") | Keyword + regex extractor (kg / tonnes / quintals, condition words, city hints) | "No technical classifications needed" is the core UX promise |
| **Image classification** (`vision.py`) | Vision model identifies waste type, condition and estimated quantity from a photo | Returns `None` (caller keeps manual fields) | Photo listing is the fastest path for a farmer with a phone |
| **Buyer ranking** (`matcher.py`) | n/a — deterministic, auditable | Multi-factor economic scoring (`scoring_config.py`, versioned weights) | Rankings must be explainable and reproducible |
| **Ranking explanation** (`explainer.py`) | LLM writes a plain-language "why this buyer" summary from the factor breakdown | Templated summary from the same breakdown | Explanations come from real numbers, never hallucinated |
| **Buyer outreach** (`messaging.py`) | LLM writes the outreach subject/body (locale-aware) | Professional template | The agent needs to sound human in many languages/contexts |
| **Negotiation** (`messaging.py`) | LLM proposes a counter-offer with rationale | Supplier rules enforced **deterministically on top** | An AI agent can only negotiate *up* from the supplier's floor — never below it |

## Where the AI agent sits

The negotiation loop (`waste2worth_agent/workflow.py`) is a **deterministic state
machine gated on human approval**:

```
supplier approval  →  outreach message (LLM)  →  buyer response
      →  accept (rule check)  OR  counter-offer (LLM proposes, rules clamp)
      →  deal confirmed / rejected  (transaction + event log)
```

The LLM decides *how to say it*; deterministic rules decide *whether a deal is
allowed*. This is the opposite of an unsafe "agent doing whatever it wants", and
it is the reason suppliers trust the system.

## Configuration

- `WASTE2WORTH_USE_AI=0` → pure rule engine, no network calls (default for tests).
- `OPENAI_API_KEY` + quota → all LLM features active; failures fall back per-call.
- `SMTP_*` vars → the agent sends real outbound email via SMTP
  (`app/services/agent_service.py`); without them, contact is simulated and
  logged as events (perfect for a demo video).

## Transparency

- `/health` reports `ai_enabled`, `openai_key_present`, `smtp_enabled`.
- Every analysis/extraction/message result carries a `source`:
  `domain_rules`, `openai_responses_api`, `nl_rules`, `openai_nl_extraction`,
  `openai_vision`, `template`, `openai_messaging`, `rule_negotiation`,
  `openai_negotiation`, `factor_rules`, `openai_explanation`.
