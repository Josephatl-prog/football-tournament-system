from app import create_app
from extensions import db
from models.team import Team

app = create_app()

all_teams = [
    "Aerospace Engineering",
    "Automotive Engineering",
    "Business Administration & Economics",
    "Chemistry",
    "Civil Engineering",
    "Computer Science",
    "Cyber Security",
    "Electrical/Electronic Engineering",
    "Information & Communication Engineering",
    "International Relations",
    "Mechanical Engineering",
    "Mechatronics Engineering",
    "Metallurgical & Materials Engineering",
    "Physics with Electronics",
    "Statistics",
    "Telecommunication Engineering"
]

with app.app_context():

    existing_names = {
        team.name
        for team in Team.query.all()
    }

    added = 0

    for name in all_teams:

        if name not in existing_names:

            team = Team(
                name=name,
                captain="",
                manager="",
                players=0,
                played=0,
                won=0,
                drawn=0,
                lost=0,
                goals_for=0,
                goals_against=0,
                goal_difference=0,
                points=0,
                group_id=None
            )

            db.session.add(team)

            added += 1

    db.session.commit()

    print(f"Added {added} missing teams.")

    print("\nAll teams:")

    for team in Team.query.order_by(Team.id).all():

        print(team.id, team.name)
