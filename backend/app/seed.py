from app.core.database import SessionLocal, engine, Base
from app.models.aircraft import AircraftModel, Fleet

def seed_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(AircraftModel).first():
        print("Database already seeded.")
        db.close()
        return

    # 1. Aircraft Models
    models = [
        # Boeing
        AircraftModel(
            manufacturer="Boeing", model="737-800", category="Narrow-body",
            range_km=5460, cruise_speed_knots=450, capacity=189, fuel_burn_kg_per_hour=2500
        ),
        AircraftModel(
            manufacturer="Boeing", model="787-9", category="Wide-body",
            range_km=14140, cruise_speed_knots=488, capacity=290, fuel_burn_kg_per_hour=5400
        ),
        # Airbus
        AircraftModel(
            manufacturer="Airbus", model="A320neo", category="Narrow-body",
            range_km=6300, cruise_speed_knots=447, capacity=180, fuel_burn_kg_per_hour=2200
        ),
        AircraftModel(
            manufacturer="Airbus", model="A350-900", category="Wide-body",
            range_km=15000, cruise_speed_knots=488, capacity=325, fuel_burn_kg_per_hour=5800
        ),
        # Embraer
        AircraftModel(
            manufacturer="Embraer", model="E195-E2", category="Regional",
            range_km=4815, cruise_speed_knots=470, capacity=146, fuel_burn_kg_per_hour=1800
        )
    ]
    
    db.add_all(models)
    db.commit()
    
    # Refresh to get IDs
    for m in models:
        db.refresh(m)
        
    # 2. Fleet
    fleet_items = [
        Fleet(tail_number="N101BA", model_id=models[0].id, status="Active"),
        Fleet(tail_number="N102BA", model_id=models[0].id, status="Maintenance"),
        Fleet(tail_number="N787DX", model_id=models[1].id, status="Active"),
        Fleet(tail_number="G-UZHA", model_id=models[2].id, status="Active"),
        Fleet(tail_number="G-UZHB", model_id=models[2].id, status="Active"),
        Fleet(tail_number="F-WWMZ", model_id=models[3].id, status="Active"),
        Fleet(tail_number="PR-E2A", model_id=models[4].id, status="Active"),
    ]
    
    db.add_all(fleet_items)
    db.commit()
    db.close()
    print("Database successfully seeded with aircraft data!")

if __name__ == "__main__":
    seed_db()
