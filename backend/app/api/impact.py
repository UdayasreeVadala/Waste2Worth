from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.transaction import Transaction
from app.models.waste import WasteListing
from app.services.ai_service import analyze_waste_listing
from waste2worth_ai.impact import estimate_impact, impact_summary

router = APIRouter()

DEAL_STATUSES = {"deal_confirmed", "pickup_scheduled", "collected", "completed"}


@router.get("/summary")
def impact_summary_endpoint(db: Session = Depends(get_db)):
    """Aggregate environmental + economic impact across all listed waste and
    confirmed deals on the platform."""
    listings = db.query(WasteListing).filter(WasteListing.status.in_(["available", "matched"])).all()
    buyers = db.query(Buyer).all()

    rows = []
    for listing in listings:
        try:
            result = analyze_waste_listing(listing, buyers)
        except Exception:
            continue
        rows.append(result["impact"])

    deals = db.query(Transaction).filter(Transaction.status.in_(DEAL_STATUSES)).all()
    deals_quantity_kg = sum((deal.quantity_kg or 0) for deal in deals)
    deals_supplier_earnings = sum((deal.supplier_earning or 0) for deal in deals)
    deals_currency = deals[0].currency if deals else "INR"

    summary = impact_summary(rows)
    summary["confirmed_deals"] = {
        "count": len(deals),
        "quantity_kg": round(deals_quantity_kg, 2),
        "supplier_earnings": round(deals_supplier_earnings, 2),
        "currency": deals_currency,
    }
    return summary
