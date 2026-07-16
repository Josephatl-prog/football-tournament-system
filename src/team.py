class Team:
    """
    Represents a football team.
    """

    def __init__(self, team_id, name, captain, manager):

        self.team_id = team_id
        self.name = name
        self.captain = captain
        self.manager = manager

        self.group = None

        # Players
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

        # Last five results
        self.form = []

    def add_player(self, player):
        """
        Adds a player to the team.
        """

        player.team = self

        self.players.append(player)

    def update_form(self, result):
        """
        Updates the team's recent form.
        """

        self.form.append(result)

        if len(self.form) > 5:
            self.form.pop(0)

    def get_form(self):
        """
        Returns the team's recent form.
        """

        return "".join(self.form)

    def display_players(self):
        """
        Displays all players in the team.
        """

        print(f"\nPlayers for {self.name}:")

        for player in self.players:
            print(player)

    def display_statistics(self):
        """
        Displays the team's statistics.
        """

        print(f"\nStatistics for {self.name}")

        print(f"Team ID: {self.team_id}")
        print(f"Group: {self.group}")

        print(f"Played: {self.played}")
        print(f"Won: {self.won}")
        print(f"Drawn: {self.drawn}")
        print(f"Lost: {self.lost}")

        print(f"Goals For: {self.goals_for}")
        print(f"Goals Against: {self.goals_against}")
        print(f"Goal Difference: {self.goal_difference}")

        print(f"Points: {self.points}")

        print(f"Form: {self.get_form()}")

    def __str__(self):
        return self.name
