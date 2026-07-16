class QualificationManager:
    """
    Determines which teams qualify from each group.
    """

    def __init__(self, tournament):
        self.tournament = tournament

    def get_qualified_teams(self):
        """
        Returns the top two teams from every group.
        """

        qualified = []

        for group in self.tournament.groups:

            standings = sorted(
                group.teams,
                key=lambda team: (
                    team.points,
                    team.goal_difference,
                    team.goals_for
                ),
                reverse=True
            )

            qualified.append({
                "group": group.name,
                "winner": standings[0],
                "runner_up": standings[1]
            })

        return qualified

    def display_qualified_teams(self):
        """
        Displays all qualified teams.
        """

        print("\n========== QUALIFIED TEAMS ==========")

        qualified = self.get_qualified_teams()

        for item in qualified:

            print(f"\nGroup {item['group']}")

            print(f"🥇 Winner     : {item['winner'].name}")

            print(f"🥈 Runner-up  : {item['runner_up'].name}")
