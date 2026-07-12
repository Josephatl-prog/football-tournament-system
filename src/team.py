class Team:
    """
    Represents a football team.
    """

    def __init__(self, name, captain, manager):
        self.name = name
        self.captain = captain
        self.manager = manager
        self.players = []
        self.group = None

    def display_info(self):
        print(f"Team Name: {self.name}")
        print(f"Captain: {self.captain}")
        print(f"Manager: {self.manager}")
        print(f"Number of Players: {len(self.players)}")
        print(f"Group: {self.group}")

    def __str__(self):
        return self.name

    def add_player(self, player):
        player.team = self
        self.players.append(player)

    def display_players(self):
        print(f"\nPlayers for {self.name}")

        if not self.players:
            print("No players registered.")
            return

        for player in self.players:
            print(player)
