from extensions import db


class Group(db.Model):

    __tablename__ = "groups"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(10),
        nullable=False,
        unique=True
    )

    teams = db.relationship(
        "Team",
        backref="group",
        lazy=True
    )

    def __repr__(self):
        return f"<Group {self.name}>"
