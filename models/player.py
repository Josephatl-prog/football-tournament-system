from extensions import db


class Player(db.Model):

    __tablename__ = "players"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    jersey_number = db.Column(
        db.Integer,
        nullable=False
    )

    position = db.Column(
        db.String(50),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    goals = db.Column(
        db.Integer,
        default=0
    )

    assists = db.Column(
        db.Integer,
        default=0
    )

    yellow_cards = db.Column(
        db.Integer,
        default=0
    )

    red_cards = db.Column(
        db.Integer,
        default=0
    )

    matches_played = db.Column(
        db.Integer,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Available"
    )
