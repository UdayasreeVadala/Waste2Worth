# Impact Model

Waste2Worth's headline environmental metric is **avoided methane**: the CH₄ that
would have been released if the organic waste had been dumped in an open landfill
or dump instead of recovered into biogas, compost, vermicompost or biochar.

All factors live in `waste2worth_ai/impact_factors.py` as named, versioned,
documented constants (`FACTOR_VERSION = 1.0.0`).

## Methodology

### Avoided emissions (primary metric)

```
methane_avoided_kg  = quantity_kg × METHANE_YIELD_PER_KG (0.10)
co2e_gwp100         = methane_avoided_kg × GWP_CH4_100 (28)
co2e_gwp20          = methane_avoided_kg × GWP_CH4_20 (81.2)
```

- `METHANE_YIELD_PER_KG = 0.10` kg CH₄ / kg wet organic waste — a conservative
  central value within the 0.05–0.20 range used across calculators, assuming an
  **uncaptured** dump (the reality in much of the target market). With landfill
  gas capture (US EPA WARM assumption of ~40%), the figure is lower (~0.05);
  without any capture it trends higher.
- GWP values are IPCC AR5: 28 (100-year) and 81.2 (20-year). We report both —
  food-waste methane has outsized short-term warming, which is exactly why
  avoiding it matters now.

### Recovery co-benefits (secondary, reported separately, never double-counted)

| Route | Co-benefit | Factor |
|---|---|---|
| Anaerobic digestion | Biogas displaces grid electricity | `AD_ELECTRICAL_KWH_PER_KG (0.15)` × `GRID_EMISSION_FACTOR (0.82 kg CO₂e/kWh, India CEA)` |
| Composting / vermicomposting | Fertiliser offset + soil carbon | `COMPOST_CO_BENEFIT (0.02 kg CO₂e/kg)` (conservative) |
| Biochar | Long-lived carbon storage | dry matter (0.25) × carbon (0.45) × stable retention (0.50) × 44/12 |

### Equivalencies (EPA GHG Equivalencies Calculator)

- `0.20 kg CO₂e` per car-kilometre
- `0.85 kg CO₂e` per coal kWh
- `21.7 kg CO₂e` sequestered per tree-year

### Economics

`estimate_margin` (`pricing.py`) derives supplier earnings from the buyer's offer
minus transport (`1.4 /km`, waived when the buyer picks up) and a documented
platform fee (`3%`). These factor values are shared between the AI layer and the
impact model from `impact_factors.py`.

## Sources

1. IPCC (2019) *Refinement to the 2006 IPCC Guidelines*, Vol. 5 (Waste) — methane
   generation potential and GWP values.
2. US EPA *WARM* model — landfilling food waste emission factors.
3. US EPA *Greenhouse Gas Equivalencies Calculator* — car-km, coal kWh, trees.
4. India Central Electricity Authority grid emission factor (~0.82 kg CO₂e/kWh).
5. Lehmann & Joseph (2009) *Biochar for Environmental Management* — carbon stability.

## Endpoints

- `GET /impact/summary` — aggregate impact across all listings + confirmed deals.
- Each listing analysis (`GET /waste/{id}/analysis`) includes an `impact` block
  with `factors.version` so the numbers can be traced to this document.
