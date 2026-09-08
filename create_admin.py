from run import app
from extensions import db
from models.user import User

with app.app_context():

    admin = User.query.filter_by(
        email="admin@afit.edu.ng"
    ).first()

    if admin:

        print("Admin already exists.")

    else:

        admin = User(
            username="admin",
            email="admin@afit.edu.ng",
            password="admin123",
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin account created successfully!")
