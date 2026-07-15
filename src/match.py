class Match:
    """
    Represents a football match.
    """

    def __init__(
        self,
        home_team,
        away_team,
        match_date,
        kickoff_time,
        venue,
        stage,
        group=None
    ):
        self.home_team = home_team
        self.away_team = away_team

        self.match_date = match_date
        self.kickoff_time = kickoff_time
        self.venue = venue

        self.stage = stage
        self.group = group

        self.home_score = 0
        self.away_score = 0

        self.status = "Not Played"

        self.goals = []
        self.yellow_cards = []
        self.red_cards = []
        self.substitutions = []

        self.player_of_the_match = None

    def record_result(self, home_score, away_score):
        """
        Records the final score and updates team statistics.
        """

        self.home_score = home_score
        self.away_score = away_score
        self.status = "Played"

        self.home_team.played += 1
        self.away_team.played += 1

        self.home_team.goals_for += home_score
        self.home_team.goals_against += away_score

        self.away_team.goals_for += away_score
        self.away_team.goals_against += home_score

        self.home_team.goal_difference = (
            self.home_team.goals_for -
            self.home_team.goals_against
        )

        self.away_team.goal_difference = (
            self.away_team.goals_for -
            self.away_team.goals_against
        )

        if home_score > away_score:

            self.home_team.won += 1
            self.home_team.points += 3

            self.away_team.lost += 1

        elif away_score > home_score:

            self.away_team.won += 1
            self.away_team.points += 3

            self.home_team.lost += 1

        else:

            self.home_team.drawn += 1
            self.away_team.drawn += 1

            self.home_team.points += 1
            self.away_team.points += 1

    def add_goal(self, scorer, minute, assist=None):
        """
        Records a goal.
        """

        goal = {
            "scorer": scorer,
            "assist": assist,
            "minute": minute
        }

        self.goals.append(goal)

        scorer.goals += 1

        if assist:
            assist.assists += 1

    def add_yellow_card(self, player, minute):
        """
        Records a yellow card.
        """

        self.yellow_cards.append({
            "player": player,
            "minute": minute
        })

        player.yellow_cards += 1

    def add_red_card(self, player, minute):
        """
        Records a red card.
        """

        self.red_cards.append({
            "player": player,
            "minute": minute
        })

        player.red_cards += 1

    def add_substitution(self, player_out, player_in, minute):
        """
        Records a substitution.
        """

        self.substitutions.append({
            "player_out": player_out,
            "player_in": player_in,
            "minute": minute
        })

    def set_player_of_the_match(self, player):
        """
        Sets the Player of the Match.
        """

        self.player_of_the_match = player

        player.player_of_the_match_awards += 1

    def display_match(self):

        print(f"\n{self.home_team} vs {self.away_team}")
        print(f"Date: {self.match_date}")
        print(f"Kickoff: {self.kickoff_time}")
        print(f"Venue: {self.venue}")
        print(f"Stage: {self.stage}")
        print(f"Group: {self.group}")
        print(f"Status: {self.status}")
        print(f"Score: {self.home_score} - {self.away_score}")

        if self.goals:

            print("\nGoals:")

            for goal in self.goals:

                print(
                    f"{goal['minute']}' ⚽ "
                    f"{goal['scorer'].name}"
                )

                if goal["assist"]:
                    print(
                        f"    Assist: "
                        f"{goal['assist'].name}"
                    )

        if self.yellow_cards:

            print("\nYellow Cards:")

            for card in self.yellow_cards:

                print(
                    f"{card['minute']}' 🟨 "
                    f"{card['player'].name}"
                )

        if self.red_cards:

            print("\nRed Cards:")

            for card in self.red_cards:

                print(
                    f"{card['minute']}' 🟥 "
                    f"{card['player'].name}"
                )

        if self.substitutions:

            print("\nSubstitutions:")

            for sub in self.substitutions:

                print(
                    f"{sub['minute']}' 🔄 "
                    f"{sub['player_out'].name} OFF"
                )

                print(
                    f"    {sub['player_in'].name} ON"
                )

        if self.player_of_the_match:

            print("\n⭐ Player of the Match:")

            print(self.player_of_the_match.name)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
