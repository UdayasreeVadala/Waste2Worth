""".\seed.py
Create demo users, buyer profiles and a sample waste listing for the Waste2Worth demo.

Run from the backend directory:

    python -m app.seed

Demo credentials:
    admin@waste2worth.dev   / admin123    (Admin)
    supplier@demo.dev       / supplier123 (Supplier - Natasha Farms)
    buyer@demo.dev          / buyer123    (Buyer - GreenBio Energy)
    ecomarket@demo.dev      / supplier123 (Supplier - GreenBasket Market)
"""

from app.db.database import SessionLocal, init_db
from app.models.buyer import Buyer
from app.models.user import User
from app.models.waste import WasteListing
from app.services.auth_service import hash_password

DEMO_USERS = [
    {
        "name": "Platform Admin",
        "email": "admin@waste2worth.dev",
        "password": "admin123",
        "role": "admin",
        "country": "India",
        "location": "Mumbai",
    },
    {
        "name": "Natasha Farms",
        "email": "supplier@demo.dev",
        "password": "supplier123",
        "role": "supplier",
        "business_type": "Farm / Wholesale market",
        "country": "India",
        "location": "Nashik, India",
        "phone": "+91 90000 00000",
    },
    {
        "name": "GreenBasket Market",
        "email": "ecomarket@demo.dev",
        "password": "supplier123",
        "role": "supplier",
        "business_type": "Supermarket",
        "country": "India",
        "location": "Nashik, India",
        "phone": "+91 90000 00001",
    },
    {
        "name": "GreenBio Energy",
        "email": "buyer@demo.dev",
        "password": "buyer123",
        "role": "buyer",
        "business_type": "Biogas plant",
        "country": "India",
        "location": "Nashik Industrial Area",
    },
    {
        "name": "EcoCompost Nashik",
        "email": "composter@demo.dev",
        "password": "buyer123",
        "role": "buyer",
        "business_type": "Composting company",
        "country": "India",
        "location": "Nashik Market Road",
    },
    {
        "name": "BioCycle Organics",
        "email": "biocycle@demo.dev",
        "password": "buyer123",
        "role": "buyer",
        "business_type": "Organic processor",
        "country": "India",
        "location": "Sinnar Road, Nashik",
    },
    {
        "name": "Vermico India",
        "email": "vermi@demo.dev",
        "password": "buyer123",
        "role": "buyer",
        "business_type": "Vermicompost producer",
        "country": "India",
        "location": "Ozhe, Nashik",
    },
]

DEMO_BUYER_PROFILES = [
    {
        "owner_email": "buyer@demo.dev",
        "business_name": "GreenBio Energy",
        "buyer_type": "Biogas plant",
        "location": "Nashik Industrial Area",
        "latitude": 20.01,
        "longitude": 73.79,
        "price_per_kg": 30,
        "min_quantity_kg": 100,
        "max_capacity_kg": 3000,
        "current_capacity_kg": 1500,
        "accepted_waste_types": "tomato,vegetable,fruit,food,onion,potato,banana,mango,organic",
        "pickup_available": True,
        "service_radius_km": 50,
        "availability_status": "available",
        "currency": "INR",
        "requirement_notes": "Accepting high-moisture fruit and vegetable waste for biogas generation.",
    },
    {
        "owner_email": "composter@demo.dev",
        "business_name": "EcoCompost Nashik",
        "buyer_type": "Composting company",
        "location": "Nashik Market Road",
        "latitude": 20.06,
        "longitude": 73.82,
        "price_per_kg": 26,
        "min_quantity_kg": 50,
        "max_capacity_kg": 2000,
        "current_capacity_kg": 900,
        "accepted_waste_types": "vegetable,fruit,food,onion,potato,organic",
        "pickup_available": False,
        "service_radius_km": 40,
        "availability_status": "available",
        "currency": "INR",
        "requirement_notes": "Accepting market vegetable waste with pickup by supplier delivery.",
    },
    {
        "owner_email": "biocycle@demo.dev",
        "business_name": "BioCycle Organics",
        "buyer_type": "Organic processor",
        "location": "Sinnar Road, Nashik",
        "latitude": 19.85,
        "longitude": 73.99,
        "price_per_kg": 28,
        "min_quantity_kg": 200,
        "max_capacity_kg": 5000,
        "current_capacity_kg": 2200,
        "accepted_waste_types": "vegetable,fruit,food,organic,grain,crop",
        "pickup_available": True,
        "service_radius_km": 70,
        "availability_status": "limited",
        "currency": "INR",
        "requirement_notes": "Fruit and vegetable waste for compost and digestate blending.",
    },
    {
        "owner_email": "vermi@demo.dev",
        "business_name": "Vermico India",
        "buyer_type": "Vermicompost producer",
        "location": "Ozhe, Nashik",
        "latitude": 19.92,
        "longitude": 73.72,
        "price_per_kg": 31,
        "min_quantity_kg": 100,
        "max_capacity_kg": 2500,
        "current_capacity_kg": 1100,
        "accepted_waste_types": "vegetable,fruit,banana,mango,organic,onion",
        "pickup_available": False,
        "service_radius_km": 40,
        "availability_status": "available",
        "currency": "INR",
        "requirement_notes": "Feedstock for vermicomposting; no manure or meat waste.",
    },
]

DEMO_LISTING = {
    "supplier_email": "supplier@demo.dev",
    "produce_type": "tomato",
    "quantity_kg": 700,
    "condition": "spoiled",
    "location": "Nashik, India",
    "latitude": 19.9975,
    "longitude": 73.7898,
    "notes": "Spoiled market tomatoes after the weekly wholesale auction.",
    "available_from": "Today",
    "available_until": "Tomorrow",
}


def run():
    init_db()
    db = SessionLocal()

    try:
        created = 0
        for user_data in DEMO_USERS:
            if db.query(User).filter(User.email == user_data["email"]).first():
                continue
            password = user_data.pop("password")
            db.add(User(**user_data, hashed_password=hash_password(password)))
            created += 1
        db.commit()

        for profile in DEMO_BUYER_PROFILES:
            owner = db.query(User).filter(User.email == profile["owner_email"]).first()
            if not owner or db.query(Buyer).filter(Buyer.business_name == profile["business_name"]).first():
                continue
            data = dict(profile)
            data.pop("owner_email")
            db.add(Buyer(owner_id=owner.id, **data))
            created += 1
        db.commit()

        supplier = db.query(User).filter(User.email == DEMO_LISTING["supplier_email"]).first()
        if supplier and not db.query(WasteListing).filter(WasteListing.produce_type == "tomato").filter(
            WasteListing.supplier_id == supplier.id
        ).first():
            data = dict(DEMO_LISTING)
            data.pop("supplier_email")
            db.add(WasteListing(supplier_id=supplier.id, **data))
            created += 1
        db.commit()

        print(f"Seed complete. {created} records created.")
        print("Admin:   admin@waste2worth.dev / admin123")
        print("Supplier: supplier@demo.dev / supplier123")
        print("Buyer:   buyer@demo.dev / buyer123")
    finally:
        db.close()


if __name__ == "__main__":
    run()