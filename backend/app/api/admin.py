from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.match import Match
from app.models.transaction import Transaction
from app.models.user import User
from app.models.waste import WasteListing
from app.services.auth_service import get_current_user

router = APIRouter()


def _require_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/stats")
def admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)

    total_suppliers = db.query(User).filter(User.role == "supplier").count()
    total_buyers = db.query(User).filter(User.role == "buyer").count()
    total_users = db.query(User).count()
    active_listings = db.query(WasteListing).filter(WasteListing.status == "available").count()
    active_matches = (
        db.query(Match)
        .filter(Match.status.in_(["match_found", "buyer_contacted", "offer_received", "deal_confirmed", "pickup_scheduled"]))
        .count()
    )
    completed = db.query(Transaction).filter(Transaction.status == "completed").count()

    recovered_kg = (
        db.query(func.coalesce(func.sum(Transaction.quantity_kg), 0))
        .filter(Transaction.status == "completed")
        .scalar()
    )
    total_amount = (
        db.query(func.coalesce(func.sum(Transaction.supplier_earning), 0))
        .filter(Transaction.status == "completed")
        .scalar()
    )
    matched_kg = db.query(func.coalesce(func.sum(WasteListing.quantity_kg), 0)).scalar()

    return {
        "total_users": total_users,
        "total_suppliers": total_suppliers,
        "total_buyers": total_buyers,
        "active_listings": active_listings,
        "active_matches": active_matches,
        "completed_transactions": completed,
        "waste_recovered_kg": round(recovered_kg, 2),
        "waste_redirected_kg": round(matched_kg, 2),
        "supplier_earnings_total": round(total_amount, 2),
    }


@router.get("/users")
def admin_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    users = db.query(User).order_by(User.created_at.desc()).all()
    return {
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "business_type": user.business_type,
                "country": user.country,
                "location": user.location,
                "created_at": str(user.created_at) if user.created_at else None,
            }
            for user in users
        ]
    }


@router.get("/listings")
def admin_listings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    listings = db.query(WasteListing).order_by(WasteListing.created_at.desc()).all()
    return {
        "listings": [
            {
                "id": listing.id,
                "produce_type": listing.produce_type,
                "quantity_kg": listing.quantity_kg,
                "condition": listing.condition,
                "location": listing.location,
                "status": listing.status,
                "created_at": str(listing.created_at) if listing.created_at else None,
            }
            for listing in listings
        ]
    }


@router.get("/transactions")
def admin_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    rows = db.query(Transaction).order_by(Transaction.created_at.desc()).all()
    return {
        "transactions": [
            {
                "id": row.id,
                "waste_type": row.waste_type,
                "quantity_kg": row.quantity_kg,
                "final_price": row.final_price,
                "currency": row.currency,
                "status": row.status,
                "pickup_method": row.pickup_method,
                "supplier_id": row.supplier_id,
                "buyer_user_id": row.buyer_user_id,
                "created_at": str(row.created_at) if row.created_at else None,
            }
            for row in rows
        ]
    }


@router.get("/impact")
def admin_impact(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)
    stats = admin_stats.__wrapped__(db=db, current_user=current_user)

    # Transparent methodology: only ONCE collected counts as diverted from disposal.
    return {
        "waste_recovered_kg": stats["waste_recovered_kg"],
        "transactions_completed": stats["completed_transactions"],
        "suppliers_active": stats["total_suppliers"],
        "buyers_active": stats["total_buyers"],
        "estimate_available_now_kg": stats["active_listings"]
        * db.query(func.coalesce(func.avg(WasteListing.quantity_kg), 0))
        .filter(WasteListing.status == "available")
        .scalar(),
        "methodology": "Impact is measured as organic waste with a completed transaction, "
        "i.e. material diverted from landfill/disposal into a processing route. "
        "Carbon or methane avoidance is only reported with a documented calculation method.",
    }