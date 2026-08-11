from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./waste2worth.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def ensure_sqlite_schema():
    if not DATABASE_URL.startswith("sqlite"):
        return

    buyer_columns = {
        "accepted_waste_types": "VARCHAR DEFAULT 'organic,vegetable,fruit,food,crop,produce'",
        "min_quantity_kg": "FLOAT DEFAULT 0",
        "current_capacity_kg": "FLOAT",
        "pickup_available": "BOOLEAN DEFAULT 1",
        "service_radius_km": "FLOAT",
        "availability_status": "VARCHAR DEFAULT 'available'",
        "currency": "VARCHAR DEFAULT 'INR'",
    }

    with engine.begin() as connection:
        existing_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(buyers)")).fetchall()
        }
        for column_name, column_type in buyer_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE buyers ADD COLUMN {column_name} {column_type}")
                )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
