"""Impact model constants and sources.

Every number below is a named, documented factor so the environmental
accounting is auditable rather than a magic constant. The headline metric is
*avoided methane*: the emissions that would have occurred if the organic waste
had been dumped in an open landfill or dump instead of recovered.

Primary reference points
------------------------
- IPCC (2019) Refinement to the 2006 Guidelines, Vol. 5 (Waste):
  default methane generation potential (L0) for landfilled organic waste and
  the 100-year Global Warming Potential of methane (GWP100 = 28, AR5).
- US EPA WARM model: "landfilling food waste" emits ~1.15 t CO2e per short ton
  assuming 40% landfill-gas capture. Open dumps (common in the target market)
  have effectively zero capture, so the no-capture figure is higher.
- EPA GHG Equivalencies Calculator for car-kilometres (0.20 kg CO2e/km) and
  tree sequestration (21.7 kg CO2/tree/year).
- India CEA grid emission factor (~0.82 kg CO2e/kWh) for the AD co-benefit.
"""

# --- Core landfill/methane ---
# kg of CH4 released per kg of wet organic waste if landfilled without capture.
# Conservative central value within the 0.05-0.20 range used across calculators.
METHANE_YIELD_PER_KG = 0.10

# Global Warming Potential of methane (IPCC AR5).
GWP_CH4_100 = 28.0
GWP_CH4_20 = 81.2

# --- Recovery co-benefits (presented separately, never double counted) ---
# Anaerobic digestion: electrical energy displaced per kg of wet organic input.
# ~0.15 kWh/kg wet feed at typical VS content and digester efficiency.
AD_ELECTRICAL_KWH_PER_KG = 0.15
# Grid emission factor used for displaced electricity (India CEA, ~2021).
GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH = 0.82

# Compost co-benefit: conservative combined fertiliser-offset + soil-carbon
# benefit per kg of wet feedstock converted to compost.
COMPOST_CO_BENEFIT_KG_CO2E_PER_KG = 0.02

# Biochar: long-lived carbon storage per kg of wet feedstock.
# dry matter fraction * carbon fraction * stable-carbon retention * 44/12.
BIOCHAR_DRY_MATTER_FRACTION = 0.25
BIOCHAR_CARBON_FRACTION = 0.45
BIOCHAR_STABLE_RETENTION = 0.50
CO2_PER_CARBON = 44.0 / 12.0

# --- Equivalency factors (EPA GHG Equivalencies Calculator) ---
KG_CO2E_PER_KM_DRIVEN = 0.20
KG_CO2E_PER_KWH_COAL = 0.85
KG_CO2E_PER_TREE_YEAR = 21.7

# --- Economic defaults ---
PLATFORM_FEE_RATE = 0.03
TRANSPORT_COST_PER_KM = 1.4

FACTOR_VERSION = "1.0.0"

FACTORS = {
    "version": FACTOR_VERSION,
    "methane_yield_per_kg": METHANE_YIELD_PER_KG,
    "gwp_ch4_100": GWP_CH4_100,
    "gwp_ch4_20": GWP_CH4_20,
    "ad_electrical_kwh_per_kg": AD_ELECTRICAL_KWH_PER_KG,
    "grid_emission_factor_kg_co2e_per_kwh": GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH,
    "compost_co_benefit_kg_co2e_per_kg": COMPOST_CO_BENEFIT_KG_CO2E_PER_KG,
    "kg_co2e_per_km_driven": KG_CO2E_PER_KM_DRIVEN,
    "kg_co2e_per_kwh_coal": KG_CO2E_PER_KWH_COAL,
    "kg_co2e_per_tree_year": KG_CO2E_PER_TREE_YEAR,
}

SOURCES = [
    "IPCC (2019) Refinement to 2006 Guidelines, Vol. 5 Waste — methane generation and GWP",
    "US EPA WARM model — landfilling food waste emission factors",
    "US EPA GHG Equivalencies Calculator — km, coal kWh, tree sequestration",
    "India CEA grid emission factor (~0.82 kg CO2e/kWh) for AD electricity offset",
    "Lehmann & Joseph (2009) Biochar for Environmental Management — carbon stability",
]
