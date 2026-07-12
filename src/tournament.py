class Tournament:
    """
    Represents a football tournament.
    """

    def __init__(self, name, year, number_of_groups, teams_per_group):
        self.name = name
        self.year = year
        self.number_of_groups = number_of_groups
        self.teams_per_group = teams_per_group
        self.teams = []
        self.groups = []

    def display_info(self):
        print(f"Tournament Name: {self.name}")
        print(f"Year: {self.year}")
        print(f"Number of Groups: {self.number_of_groups}")
        print(f"Teams Per Group: {self.teams_per_group}")

    def add_team(self, team):
        self.teams.append(team)

    def display_teams(self):
        print("\nRegistered Teams:")

        if not self.teams:
            print("No teams have been registered yet.")
            return

        for team in self.teams:
            print(f"- {team}")

    def add_group(self, group):
        self.groups.append(group)
