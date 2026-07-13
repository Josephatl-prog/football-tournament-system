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

    def display_table(self):
        """
        Displays the current league table for the group.
        """

        # Sort teams
        sorted_teams = sorted(
            self.teams,
            key=lambda team: (
                team.points,
                team.goal_difference,
                team.goals_for
            ),
            reverse=True
        )

        print(f"\n================ GROUP {self.name} ================\n")

        print(
            f"{'Team':<28}"
            f"{'P':>3}"
            f"{'W':>4}"
            f"{'D':>4}"
            f"{'L':>4}"
            f"{'GF':>5}"
            f"{'GA':>5}"
            f"{'GD':>5}"
            f"{'PTS':>6}"
        )

        print("-" * 65)

        for team in sorted_teams:

            print(
                f"{team.name:<28}"
                f"{team.played:>3}"
                f"{team.won:>4}"
                f"{team.drawn:>4}"
                f"{team.lost:>4}"
                f"{team.goals_for:>5}"
                f"{team.goals_against:>5}"
                f"{team.goal_difference:>5}"
                f"{team.points:>6}"
            )

    def __str__(self):
        return f"Group {self.name}"
