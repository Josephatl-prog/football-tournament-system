class Team:
    """
    Represents a football team.
    """

    def __init__(self, team_id, name, captain, manager):
        self.team_id = team_id
        self.name = name
        self.captain = captain
        self.manager = manager

        # Tournament Group
        self.group = None

        # Squad
        self.players = []

        # Team Statistics
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0

        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0

        self.points = 0

    def add_player(self, player):
        """
        Adds a player to the team.
        """
        player.team = self.name
        self.players.append(player)

    def display_players(self):
        """
        Displays all players in the team.
        """
        print(f"\nPlayers for {self.name}:")

        if not self.players:
            print("No players registered.")
            return

        for player in self.players:
            print(player)

    def display_statistics(self):
        """
        Displays the team's tournament statistics.
        """
        print(f"\nStatistics for {self.name}")
        print(f"Team ID: {self.team_id}")
        print(f"Group: {self.group}")
        print(f"Captain: {self.captain}")
        print(f"Manager: {self.manager}")
        print(f"Played: {self.played}")
        print(f"Won: {self.won}")
        print(f"Drawn: {self.drawn}")
        print(f"Lost: {self.lost}")
        print(f"Goals For: {self.goals_for}")
        print(f"Goals Against: {self.goals_against}")
        print(f"Goal Difference: {self.goal_difference}")
        print(f"Points: {self.points}")

    def __str__(self):
        return self.name
