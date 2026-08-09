from waste2worth_ai.errors import ContractError
from waste2worth_ai.geo import distance_km
from waste2worth_ai.schemas import BuyerProfile, SupplierRules, WasteInput
from waste2worth_ai.status import AVAILABLE_BUYER_STATUSES


def parse_waste_input(data):
    _require(data, "waste_type")
    _require(data, "quantity_kg")
    quantity_kg = _positive_float(data["quantity_kg"], "quantity_kg")

    return WasteInput(
        supplier_id=data.get("supplier_id"),
        waste_type=str(data["waste_type"]).strip().lower(),
        quantity_kg=quantity_kg,
        condition=str(data.get("condition", "unknown")).strip().lower(),
        location=dict(data.get("location", {})),
        available_from=data.get("available_from"),
        available_until=data.get("available_until"),
        photo_url=data.get("photo_url"),
        notes=data.get("notes"),
    )


def parse_buyer(data):
    required_fields = [
        "id",
        "name",
        "business_type",
        "accepted_waste",
        "min_quantity_kg",
        "max_quantity_kg",
        "current_capacity_kg",
        "price_per_kg",
    ]
    for field in required_fields:
        _require(data, field)

    availability_status = str(data.get("availability_status", "available")).lower()
    if availability_status not in AVAILABLE_BUYER_STATUSES:
        raise ContractError(
            "INVALID_BUYER_STATUS",
            f"availability_status must be one of {sorted(AVAILABLE_BUYER_STATUSES)}.",
            "availability_status",
        )

    accepted_waste = [str(item).strip().lower() for item in data["accepted_waste"]]
    if not accepted_waste:
        raise ContractError("EMPTY_ACCEPTED_WASTE", "accepted_waste cannot be empty.", "accepted_waste")

    min_quantity_kg = _non_negative_float(data["min_quantity_kg"], "min_quantity_kg")
    max_quantity_kg = _positive_float(data["max_quantity_kg"], "max_quantity_kg")
    if min_quantity_kg > max_quantity_kg:
        raise ContractError(
            "INVALID_QUANTITY_RANGE",
            "min_quantity_kg cannot be greater than max_quantity_kg.",
            "min_quantity_kg",
        )

    location = dict(data.get("location", {}))
    parsed_distance = data.get("distance_km")
    if parsed_distance is not None:
        parsed_distance = _non_negative_float(parsed_distance, "distance_km")

    return BuyerProfile(
        id=str(data["id"]),
        name=str(data["name"]),
        business_type=str(data["business_type"]),
        location=location,
        distance_km=parsed_distance,
        accepted_waste=accepted_waste,
        min_quantity_kg=min_quantity_kg,
        max_quantity_kg=max_quantity_kg,
        current_capacity_kg=_non_negative_float(data["current_capacity_kg"], "current_capacity_kg"),
        price_per_kg=_non_negative_float(data["price_per_kg"], "price_per_kg"),
        currency=str(data.get("currency", "USD")),
        pickup_available=bool(data.get("pickup_available", False)),
        service_radius_km=(
            _positive_float(data["service_radius_km"], "service_radius_km")
            if data.get("service_radius_km") is not None
            else None
        ),
        availability_status=availability_status,
        last_updated=data.get("last_updated"),
    )


def parse_supplier_rules(data):
    _require(data, "minimum_total_price")
    return SupplierRules(
        minimum_total_price=_non_negative_float(data["minimum_total_price"], "minimum_total_price"),
        requires_pickup=bool(data.get("requires_pickup", False)),
        allow_counter_offer=bool(data.get("allow_counter_offer", True)),
    )


def resolve_buyer_distances(waste_input, buyers):
    resolved = []
    for buyer in buyers:
        if buyer.distance_km is not None:
            resolved.append(buyer)
            continue

        calculated_distance = distance_km(waste_input.location, buyer.location)
        if calculated_distance is None:
            raise ContractError(
                "MISSING_DISTANCE",
                "Buyer must include distance_km or both waste and buyer locations must include coordinates.",
                "distance_km",
            )

        resolved.append(
            BuyerProfile(
                id=buyer.id,
                name=buyer.name,
                business_type=buyer.business_type,
                location=buyer.location,
                distance_km=calculated_distance,
                accepted_waste=buyer.accepted_waste,
                min_quantity_kg=buyer.min_quantity_kg,
                max_quantity_kg=buyer.max_quantity_kg,
                current_capacity_kg=buyer.current_capacity_kg,
                price_per_kg=buyer.price_per_kg,
                currency=buyer.currency,
                pickup_available=buyer.pickup_available,
                service_radius_km=buyer.service_radius_km,
                availability_status=buyer.availability_status,
                last_updated=buyer.last_updated,
            )
        )
    return resolved


def _require(data, field):
    if field not in data or data[field] is None:
        raise ContractError("MISSING_FIELD", f"{field} is required.", field)
    if isinstance(data[field], str) and data[field].strip() == "":
        raise ContractError("MISSING_FIELD", f"{field} is required.", field)


def _positive_float(value, field):
    number = _as_float(value, field)
    if number <= 0:
        raise ContractError("INVALID_NUMBER", f"{field} must be greater than zero.", field)
    return number


def _non_negative_float(value, field):
    number = _as_float(value, field)
    if number < 0:
        raise ContractError("INVALID_NUMBER", f"{field} cannot be negative.", field)
    return number


def _as_float(value, field):
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ContractError("INVALID_NUMBER", f"{field} must be a number.", field) from exc
