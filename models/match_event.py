from extensions import db


class MatchEvent(db.Model):

    __tablename__ = "match_events"

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

    event_type = db.Column(
        db.String(30),
        nullable=False
    )

    minute = db.Column(
        db.Integer
    )

    assist_player_id = db.Column(
        db.Integer,
        db.ForeignKey("players.id"),
        nullable=True
    )

    fixture = db.relationship(
        "Fixture",
        backref="events"
    )

    player = db.relationship(
        "Player",
        foreign_keys=[player_id]
    )

    assist_player = db.relationship(
        "Player",
        foreign_keys=[assist_player_id]
    )

    def __repr__(self):

        return (
            f"<MatchEvent "
            f"{self.event_type} "
            f"Player {self.player_id}>"
        )
