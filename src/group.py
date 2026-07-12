class Group:
    """
    Represents a tournament group.
    """

    def __init__(self, name):
        self.name = name
        self.teams = []

    def add_team(self, team):
        team.group = self.name
        self.teams.append(team)

    def display_teams(self):
        print(f"\nGroup {self.name}")

        if not self.teams:
            print("No teams assigned.")
            return

        for team in self.teams:
            print(f"- {team}")

    def __str__(self):
        return f"Group {self.name}"
