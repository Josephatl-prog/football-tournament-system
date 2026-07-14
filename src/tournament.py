from src.group import Group


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
        """
        Registers a team in the tournament.
        """
        self.teams.append(team)

    def display_teams(self):
        """
        Displays all registered teams.
        """
        print("\nRegistered Teams:")

        if not self.teams:
            print("No teams have been registered yet.")
            return

        for team in self.teams:
            print(f"- {team}")

    def create_group(self, group_name):
        """
        Creates a new group.
        """
        group = Group(group_name)
        self.groups.append(group)
        return group

    def get_group(self, group_name):
        """
        Returns a group by name.
        """
        for group in self.groups:
            if group.name == group_name:
                return group

        return None

    def get_team_by_id(self, team_id):
        """
        Returns a team using its team ID.
        """
        for team in self.teams:
            if team.team_id == team_id:
                return team

        return None

    def assign_team_to_group(self, team_id, group_name):
        """
        Assigns a team to a group.
        """
        team = self.get_team_by_id(team_id)
        group = self.get_group(group_name)

        if team is None:
            print(f"Team '{team_id}' not found.")
            return

        if group is None:
            print(f"Group '{group_name}' not found.")
            return

        group.add_team(team)

    def display_groups(self):
        """
        Displays all tournament groups.
        """
        print("\nTournament Groups:")

        if not self.groups:
            print("No groups created.")
            return

        for group in self.groups:
            print(group)
