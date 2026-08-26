from extensions import db


class Team(db.Model):

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    captain = db.Column(db.String(100))

    manager = db.Column(db.String(100))

    players = db.Column(db.Integer, default=0)

    group_id = db.Column(
        db.Integer,
        db.ForeignKey("groups.id"),
        nullable=True
    )

    # Tournament Statistics

    played = db.Column(db.Integer, default=0)

    won = db.Column(db.Integer, default=0)

    drawn = db.Column(db.Integer, default=0)

    lost = db.Column(db.Integer, default=0)

    goals_for = db.Column(db.Integer, default=0)

    goals_against = db.Column(db.Integer, default=0)

    goal_difference = db.Column(db.Integer, default=0)

    points = db.Column(db.Integer, default=0)

    # Relationship to players

    players_list = db.relationship(
        "Player",
        backref="team",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Team {self.name}>"
