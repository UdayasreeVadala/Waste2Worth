# Waste2Worth

### Give Waste a Second Life.

Waste2Worth is an AI-powered organic waste recovery platform that connects suppliers with organic waste to buyers who can reuse that material as a raw input.

The platform does more than list waste. It analyzes the waste, recommends the best practical processing route, ranks suitable buyers, estimates supplier earnings, and uses an agent workflow to coordinate buyer contact after supplier approval.

## Core Flow

```text
Waste listing
  ->
AI analysis
  ->
Possible uses
  ->
Buyer ranking
  ->
Supplier approval
  ->
AI agent contact
  ->
Offer / negotiation
  ->
Deal confirmation
```

## What The AI Does

- Builds a structured waste profile
- Identifies suitable processing routes
- Compares buyer demand, distance, capacity, pickup, and pricing
- Estimates supplier net earnings
- Returns ranked buyer matches with explanations

## What The Agent Does

- Waits for supplier approval before contacting a buyer
- Sends waste details to the selected buyer
- Evaluates the buyer offer against supplier rules
- Sends a counter offer when allowed
- Updates transaction status
- Emits activity events for the UI

## Current Project Structure

```text
waste2worth/
|
|-- app/                  # FastAPI backend plus Next.js app route files
|-- waste2worth_ai/       # AI analysis, recommendation, matching, pricing
|-- waste2worth_agent/    # Agent workflow and negotiation
|-- docs/                 # API and integration contracts
|-- tests/                # AI/agent tests
|-- package.json          # Frontend dependencies
|-- requirements.txt      # Backend dependencies
|-- run_tests.py          # Lightweight AI/agent test runner
`-- README.md
```

## Backend

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Main backend routes:

```text
/auth
/waste
/buyers
/matches
/agent
```

The backend connects to the AI module through:

```text
app/services/ai_service.py
```

## Frontend

Install dependencies:

```bash
npm install
```

Run the Next.js app:

```bash
npm run dev
```

The frontend entry point is:

```text
app/page.tsx
```

## Verification

Run the lightweight AI/agent tests:

```bash
python run_tests.py
```

Current covered cases:

- full AI pipeline
- no suitable buyers
- buyer outside service radius
- coordinate-based distance calculation
- invalid quantity rejection
- supplier approval guard
- accepted offer
- rejected offer
- event logging

## Integration Notes

See:

```text
docs/API_CONTRACT.md
docs/AGENT_CONTRACT.md
docs/INTEGRATION_NOTES.md
```
