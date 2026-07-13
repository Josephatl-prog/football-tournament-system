class Team:
    """
    Represents a football team.
    """

    def __init__(self, name, captain, manager):
        self.name = name
        self.captain = captain
        self.manager = manager

        # List to store players
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
        self.players.append(player)

    def display_players(self):
        """
        Displays all players in the team.
        """
        print(f"\nPlayers for {self.name}:")

        for player in self.players:
            print(player)

    def display_statistics(self):
        """
        Displays the team's tournament statistics.
        """
        print(f"\nStatistics for {self.name}")
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
