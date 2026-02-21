"""
Database seeding script
Populates the database with football club data
"""
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models.club import Club


def seed_clubs(db: Session):
    """Seed the database with football clubs"""

    clubs_data = [
        {"name": "Manchester United", "logo_path": "/static/logos/manchester_united.png"},
        {"name": "Liverpool", "logo_path": "/static/logos/liverpool.png"},
        {"name": "Barcelona", "logo_path": "/static/logos/barcelona.png"},
        {"name": "Real Madrid", "logo_path": "/static/logos/real_madrid.png"},
        {"name": "Bayern Munich", "logo_path": "/static/logos/bayern_munich.png"},
        {"name": "Juventus", "logo_path": "/static/logos/juventus.png"},
        {"name": "Paris Saint-Germain", "logo_path": "/static/logos/psg.png"},
        {"name": "Chelsea", "logo_path": "/static/logos/chelsea.png"},
        {"name": "Arsenal", "logo_path": "/static/logos/arsenal.png"},
        {"name": "Manchester City", "logo_path": "/static/logos/manchester_city.png"},
        {"name": "AC Milan", "logo_path": "/static/logos/ac_milan.png"},
        {"name": "Inter Milan", "logo_path": "/static/logos/inter_milan.png"},
        {"name": "Ajax", "logo_path": "/static/logos/ajax.png"},
        {"name": "Borussia Dortmund", "logo_path": "/static/logos/borussia_dortmund.png"},
        {"name": "Atletico Madrid", "logo_path": "/static/logos/atletico_madrid.png"},
        {"name": "Tottenham Hotspur", "logo_path": "/static/logos/tottenham.png"},
        {"name": "Benfica", "logo_path": "/static/logos/benfica.png"},
        {"name": "Porto", "logo_path": "/static/logos/porto.png"},
        {"name": "Celtic", "logo_path": "/static/logos/celtic.png"},
        {"name": "Rangers", "logo_path": "/static/logos/rangers.png"},
    ]

    # Check if clubs already exist
    existing_count = db.query(Club).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} clubs. Skipping seed.")
        return

    # Add clubs
    for club_data in clubs_data:
        club = Club(**club_data)
        db.add(club)

    db.commit()
    print(f"Successfully seeded {len(clubs_data)} clubs!")


def main():
    """Main seeding function"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    print("Seeding database...")
    db = SessionLocal()
    try:
        seed_clubs(db)
    finally:
        db.close()

    print("Seeding complete!")


if __name__ == "__main__":
    main()