import base64
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.buyer import Buyer
from app.models.user import User
from app.models.waste import WasteListing
from app.schemas.waste import WasteCreate, WasteResponse, WasteUpdate
from app.services.ai_service import analyze_waste_listing
from app.services.auth_service import get_current_user
from waste2worth_ai.nl_extractor import extract_waste_from_text
from waste2worth_ai.vision import build_data_uri, classify_waste_image

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "static" / "uploads"
DEFAULT_COORDS = {"latitude": 19.9975, "longitude": 73.7898}


def _coerce_coords(payload: WasteCreate):
    latitude = payload.latitude if payload.latitude is not None else DEFAULT_COORDS["latitude"]
    longitude = payload.longitude if payload.longitude is not None else DEFAULT_COORDS["longitude"]
    return latitude, longitude


def _resolve_photo_data_uri(photo_url):
    """If the photo lives on this server, return it as a base64 data URI for the
    vision model. Remote URLs are passed through untouched."""
    if not photo_url:
        return None
    if photo_url.startswith(("http://", "https://", "data:")):
        return photo_url
    path = Path(__file__).resolve().parents[2] / photo_url.lstrip("/")
    if path.is_file():
        return build_data_uri(path.read_bytes())
    return None


def _smart_intake(payload: WasteCreate):
    """Enrich a listing with AI extraction. Fills only gaps the supplier left
    blank, and never overrides explicit user input."""
    enriched = {"source": None, "fields": {}}

    if payload.description:
        extraction = extract_waste_from_text(payload.description)
        if extraction:
            enriched["source"] = extraction.get("source")
            fields = enriched["fields"]
            if not payload.produce_type and extraction.get("waste_type"):
                fields["produce_type"] = extraction["waste_type"]
            if payload.quantity_kg is None and extraction.get("quantity_kg"):
                fields["quantity_kg"] = extraction["quantity_kg"]
            if payload.condition in ("unknown", "") and extraction.get("condition"):
                fields["condition"] = extraction["condition"]
            if not payload.location and extraction.get("location"):
                fields["location"] = extraction["location"]

    if not payload.produce_type and not payload.description:
        image_source = _resolve_photo_data_uri(payload.photo_url)
        if image_source:
            classification = classify_waste_image(image_source)
            if classification:
                enriched["source"] = classification.get("source")
                fields = enriched["fields"]
                fields["produce_type"] = classification.get("waste_type", "organic")
                if payload.condition in ("unknown", "") and classification.get("condition"):
                    fields["condition"] = classification["condition"]
                if payload.quantity_kg is None and classification.get("estimated_quantity_kg"):
                    fields["quantity_kg"] = classification["estimated_quantity_kg"]

    return enriched


@router.post("/", response_model=WasteResponse)
def create_waste_listing(
    waste: WasteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "supplier":
        raise HTTPException(status_code=403, detail="Only suppliers can create waste listings")

    intake = _smart_intake(waste)
    fields = intake["fields"]

    produce_type = (waste.produce_type or fields.get("produce_type") or "organic").strip().lower()
    quantity_kg = waste.quantity_kg if waste.quantity_kg is not None else fields.get("quantity_kg")
    if quantity_kg is None:
        raise HTTPException(status_code=422, detail="quantity_kg is required (or describe the waste and let AI extract it)")

    condition = waste.condition if waste.condition not in ("", "unknown") else fields.get("condition", "unknown")
    location = waste.location or fields.get("location") or current_user.location or "Nashik, India"
    latitude, longitude = _coerce_coords(waste)
    notes = waste.notes or (f"AI-extracted from description ({intake['source']})" if intake["source"] else None)

    new_waste = WasteListing(
        supplier_id=current_user.id,
        produce_type=produce_type,
        quantity_kg=quantity_kg,
        condition=condition,
        location=location,
        latitude=latitude,
        longitude=longitude,
        notes=notes,
        available_from=waste.available_from,
        available_until=waste.available_until,
        photo_url=waste.photo_url,
        status="available",
    )

    db.add(new_waste)
    db.commit()
    db.refresh(new_waste)
    return new_waste


@router.post("/upload")
def upload_photo(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "photo.jpg").suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{suffix}"
    destination = UPLOAD_DIR / filename
    destination.write_bytes(file.file.read())

    url = f"/static/uploads/{filename}"
    detection = classify_waste_image(_resolve_photo_data_uri(url))

    return {"url": url, "filename": filename, "detection": detection}


class ExtractRequest(BaseModel):
    text: str


@router.post("/extract")
def extract_listing_from_text(request: ExtractRequest):
    """AI extraction of structured listing fields from a plain-English description."""
    result = extract_waste_from_text(request.text)
    if not result:
        raise HTTPException(status_code=422, detail="Could not extract waste details from that text")
    return result


@router.get("/my-listings", response_model=list[WasteResponse])
def get_my_listings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(WasteListing).filter(WasteListing.supplier_id == current_user.id).all()


@router.get("/available", response_model=list[WasteResponse])
def get_available_listings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {"buyer", "admin", "supplier"}:
        raise HTTPException(status_code=403, detail="Not allowed")

    listings = (
        db.query(WasteListing)
        .filter(WasteListing.status.in_(["available", "matched"]))
        .order_by(WasteListing.created_at.desc())
        .all()
    )

    if current_user.role == "supplier":
        listings = [listing for listing in listings if listing.supplier_id != current_user.id]

    return listings


@router.get("/{waste_id}", response_model=WasteResponse)
def get_waste_listing(
    waste_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    waste = db.query(WasteListing).filter(WasteListing.id == waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")
    return waste


@router.patch("/{waste_id}", response_model=WasteResponse)
def update_waste_listing(
    waste_id: int,
    updates: WasteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    waste = db.query(WasteListing).filter(WasteListing.id == waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")
    if waste.supplier_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own waste listings")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(waste, field, value)

    db.commit()
    db.refresh(waste)
    return waste


@router.get("/{waste_id}/analysis")
def get_waste_analysis(
    waste_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    waste = db.query(WasteListing).filter(WasteListing.id == waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")

    if current_user.role != "admin" and waste.supplier_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view analysis for your own listings")

    buyers = db.query(Buyer).all()
    result = analyze_waste_listing(waste, buyers)

    return _analysis_payload(waste, result)


@router.post("/{waste_id}/analyze")
def reanalyze_waste(
    waste_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    waste = db.query(WasteListing).filter(WasteListing.id == waste_id).first()
    if not waste:
        raise HTTPException(status_code=404, detail="Waste listing not found")
    if current_user.role != "admin" and waste.supplier_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    buyers = db.query(Buyer).all()
    result = analyze_waste_listing(waste, buyers)
    return _analysis_payload(waste, result)


def _analysis_payload(waste, result):
    return {
        "waste": WasteResponse.model_validate(waste).model_dump(),
        "analysis": result["analysis"],
        "recommended_use": result["recommended_use"],
        "ranked_buyers": result["ranked_buyers"],
        "best_buyer": result["best_buyer"],
        "impact": result["impact"],
        "explanation": result["explanation"],
        "requires_supplier_approval": result["requires_supplier_approval"],
        "agent_status": result["agent_status"],
        "error": result["error"],
    }