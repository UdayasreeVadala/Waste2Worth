# Waste2Worth — Give Waste a Second Life

**Waste2Worth** is an AI-powered organic waste recovery platform that connects
suppliers with organic waste to the buyers who can reuse that material as a raw
input — biogas plants, composters, vermicompost and biochar producers.

It does far more than list waste. It **analyzes the waste** (from text or a
photo), **recommends the best processing route**, **ranks buyers by true net
return**, **quantifies the environmental impact** of every listing, and uses a
**human-approved AI agent** to contact and negotiate with buyers — all with
source-level transparency about what the AI did and what the rules did.

```
"around 700 kg of spoiled tomatoes near Nashik"
        │  (AI extraction — text or photo)
        ▼
structured waste profile
        │  (AI analysis + route recommendation)
        ▼
best use (biogas / compost / vermicompost / biochar)
        │  (economic scoring + explanation)
        ▼
ranked buyers with net earnings + impact (kg CO₂e avoided)
        │  (supplier approval gate)
        ▼
AI agent contacts buyer → offer → negotiation (LLM proposes, rules enforce)
        ▼
deal confirmed → tracked to pickup → completed
```

---

## Why it matters

Organic waste is a **mispriced asset**. Markets, farms and supermarkets discard
tonnes of reusable material that, dumped in an open landfill, turns into methane
— a greenhouse gas **~28× stronger than CO₂** (81× over 20 years). Waste2Worth
makes recovery the economically rational choice by paying suppliers, giving
buyers reliable feedstock, and putting a **kg CO₂e number on every listing** so
the environmental win is as visible as the price.

## What the AI does

- **Natural-language intake** — "2 tonnes of spoiled onions from Nashik" becomes a
  structured listing (`nl_extractor.py`). No dropdowns, no jargon.
- **Photo classification** — a phone photo of a waste pile yields type, condition
  and an estimated quantity (`vision.py`).
- **Structured analysis** — waste properties, suitable uses, limitations
  (`analyzer.py` + knowledge base).
- **Route recommendation** — compares processing routes against buyer demand,
  capacity, pickup and economics (`recommender.py`).
- **Economic ranking** — buyers scored on net supplier earnings, distance,
  pickup, capacity and availability with a **documented, versioned scoring model**
  (`scoring_config.py`) and an auditable factor breakdown per buyer.
- **Plain-language explanations** — LLM-written "why this buyer" summaries derived
  from real factor contributions (`explainer.py`).
- **Impact quantification** — methane avoided, CO₂e (100 & 20-year lens),
  route co-benefits, and real-world equivalencies for every listing
  (`impact.py`, `impact_factors.py`).

## What the agent does

`waste2worth_agent/workflow.py` runs a **deterministic, approval-gated state
machine**:

- waits for **supplier approval** before contacting anyone
- **LLM-writes** the outreach message (locale-aware)
- evaluates the buyer's offer against **supplier-set rules**
- **LLM proposes** a counter-offer, **rules clamp it** to the supplier's floor —
  the agent can negotiate *up*, never *down*
- updates transaction status and logs a full event/transcript trail

Outbound email is real when `SMTP_*` is configured; otherwise contact is
simulated and fully logged — perfect for a demo.

## Honesty by construction

Every AI output carries a `source` (`domain_rules`, `openai_responses_api`,
`nl_rules`, `openai_vision`, `template`, `openai_messaging`, …) and `/health`
reports what's active. The whole system runs with **zero external dependencies**
and upgrades to LLM intelligence when an API key with quota is configured.
See `backend/docs/AI_USAGE.md`.

---

## Repository layout

```
.
|-- backend/
|   |-- app/                  # FastAPI app (auth, waste, buyers, matches,
|   |   |                      #  agent, transactions, messages, admin, impact)
|   |-- waste2worth_ai/       # AI analysis, extraction, vision, ranking, impact
|   |-- waste2worth_agent/    # Agent workflow, messaging, negotiation, gateways
|   |-- docs/                 # API / agent contracts + AI usage + impact model
|   |-- tests/                # AI / agent / impact test suite
|   |-- run_tests.py          # Zero-dependency test runner
|   |-- streamlit_app.py      # Standalone Streamlit demo
|   `-- requirements.txt
|-- frontend/                 # Next.js app (supplier, buyer, admin, landing)
|-- netlify.toml              # Frontend deploy config
|-- render.yaml               # Backend deploy config
`-- .env.example
```

## Backend

```bash
cd backend
pip install -r requirements.txt
python run_tests.py          # 30 tests, zero network needed
uvicorn app.main:app --reload
```

Key routes:

```
/auth        /waste        /buyers      /matches
/agent       /transactions /messages    /admin      /impact
```

Highlights:

- `POST /waste/extract` — AI extraction from a plain-English description
- `POST /waste/upload` — upload a photo; returns AI detection alongside the URL
- `POST /waste/` — create a listing; empty fields are AI-enriched from `description` / `photo_url`
- `GET /waste/{id}/analysis` — analysis + ranking + **impact** + **explanation**
- `GET /impact/summary` — platform-wide environmental + economic dashboard
- `GET /health` — AI / SMTP configuration status

## Frontend

```bash
cd frontend
npm install
npm run dev                 # http://localhost:3000
```

The landing page is `app/page.tsx`. The supplier "Add waste" flow
(`app/supplier/add-waste`) now supports **describe-in-your-own-words auto-fill**
and **photo upload with AI detection**; the analysis page shows impact cards,
explanations and the agent controls.

## Verification

```bash
cd backend && python run_tests.py
cd frontend && npx tsc --noEmit
```

Covered cases: full AI pipeline · no suitable buyers · outside service radius ·
coordinate distance · invalid quantity · supplier-approval guard · accept/reject
offer · counter-offer floor · event logging · impact math (CH₄/CO₂e/equivalencies)
· NL extraction (kg/tonnes/quintals, cities) · photo data-URI · vision fallback ·
LLM message templates · scoring factor breakdowns.

## Docs

```
backend/docs/API_CONTRACT.md
backend/docs/AGENT_CONTRACT.md
backend/docs/INTEGRATION_NOTES.md
backend/docs/AI_USAGE.md       # what's AI vs rules, and how to tell
backend/docs/IMPACT_MODEL.md   # the environmental accounting, with sources
```
