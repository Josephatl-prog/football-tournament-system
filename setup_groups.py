from app import create_app
from extensions import db
from models.group import Group

app = create_app()

with app.app_context():

    existing_groups = Group.query.all()

    if not existing_groups:

        db.session.add_all([
            Group(name="A"),
            Group(name="B"),
            Group(name="C"),
            Group(name="D")
        ])

        db.session.commit()

        print("Groups A-D created successfully!")

    else:

        print("Groups already exist.")

    groups = Group.query.order_by(Group.id).all()

    for group in groups:

        print(group.id, group.name)
