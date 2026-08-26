from extensions import db


class Lineup(db.Model):

    __tablename__ = "lineups"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fixture_id = db.Column(
        db.Integer,
        db.ForeignKey("fixtures.id"),
        nullable=False
    )

    player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    position = db.Column(
        db.String(20),
        nullable=False
    )

    is_starting = db.Column(
        db.Boolean,
        default=True
    )

    fixture = db.relationship(
        "Fixture",
        backref="lineups"
    )

    player = db.relationship(
        "Player"
    )

    team = db.relationship(
        "Team"
    )

    def __repr__(self):
        return (
            f"<Lineup fixture={self.fixture_id} "
            f"player={self.player_id} "
            f"position={self.position}>"
        )
