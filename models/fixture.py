from extensions import db


class Fixture(db.Model):

    __tablename__ = "fixtures"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    home_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    away_team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    match_date = db.Column(
        db.String(30)
    )

    kickoff_time = db.Column(
        db.String(20)
    )

    venue = db.Column(
        db.String(100)
    )

    stage = db.Column(
        db.String(30),
        default="Group Stage"
    )

    status = db.Column(
        db.String(20),
        default="Upcoming"
    )

    home_score = db.Column(
        db.Integer,
        default=0
    )

    away_score = db.Column(
        db.Integer,
        default=0
    )

    home_team = db.relationship(
        "Team",
        foreign_keys=[home_team_id]
    )

    away_team = db.relationship(
        "Team",
        foreign_keys=[away_team_id]
    )

    lineup_published = db.Column(
        db.Boolean,
        default=False
    )
