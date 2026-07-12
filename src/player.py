class Player:
    """
    Represents a football player.
    """

    def __init__(self, name, jersey_number, position):
        self.name = name
        self.jersey_number = jersey_number
        self.position = position

        self.team = None
        self.photo = None
        self.status = "Active"

    def __str__(self):
        return f"#{self.jersey_number} {self.name} ({self.position})"
