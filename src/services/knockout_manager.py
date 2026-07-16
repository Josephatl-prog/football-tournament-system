from src.match import Match


class KnockoutManager:
    """
    Manages the knockout stage.
    """

    def __init__(self, tournament):
        self.tournament = tournament

        self.quarter_finals = []
        self.semi_finals = []
        self.third_place = None
        self.final = None

    def create_quarter_final(
        self,
        fixture_id,
        home_team,
        away_team,
        match_date,
        kickoff_time,
        venue
    ):

        match = Match(
            fixture_id=fixture_id,
            home_team=home_team,
            away_team=away_team,
            match_date=match_date,
            kickoff_time=kickoff_time,
            venue=venue,
            stage="Quarter Final"
        )

        self.quarter_finals.append(match)

        self.tournament.add_match(match)

        return match

    def display_quarter_finals(self):

        print("\n========== QUARTER FINALS ==========")

        if not self.quarter_finals:
            print("No quarter-final fixtures created.")
            return

        for match in self.quarter_finals:
            print(match)

    def get_quarter_final_winners(self):
        """
        Returns all quarter-final winners.
        """

        winners = []

        for match in self.quarter_finals:

            if match.status != "Completed":
                continue

            if match.home_score > match.away_score:
                winners.append(match.home_team)

            elif match.away_score > match.home_score:
                winners.append(match.away_team)

        return winners

    def display_quarter_final_winners(self):

        print("\n========== QUARTER FINAL WINNERS ==========")

        winners = self.get_quarter_final_winners()

        if not winners:

            print("No winners yet.")
            return

        for team in winners:

            print(f"✅ {team.name}")

    def generate_semi_finals(
        self,
        match_date,
        kickoff_time,
        venue
    ):
        """
        Generates the semi-finals automatically
        from the quarter-final winners.
        """

        winners = self.get_quarter_final_winners()

        if len(winners) != 4:

            print("Semi-finals cannot be generated yet.")

            return

        sf1 = Match(
            fixture_id="SF001",
            home_team=winners[0],
            away_team=winners[1],
            match_date=match_date,
            kickoff_time=kickoff_time,
            venue=venue,
            stage="Semi Final"
        )

        sf2 = Match(
            fixture_id="SF002",
            home_team=winners[2],
            away_team=winners[3],
            match_date=match_date,
            kickoff_time=kickoff_time,
            venue=venue,
            stage="Semi Final"
        )

        self.semi_finals = [sf1, sf2]

        self.tournament.add_match(sf1)
        self.tournament.add_match(sf2)

        print("\nSemi-finals generated successfully.")

    def display_semi_finals(self):

        print("\n========== SEMI FINALS ==========")

        if not self.semi_finals:

            print("No semi-final fixtures.")

            return

        for match in self.semi_finals:

            print(match)

    def get_semi_final_winners(self):
        """
        Returns the semi-final winners.
        """

        winners = []

        for match in self.semi_finals:

            if match.status != "Completed":
                continue

            if match.home_score > match.away_score:
                winners.append(match.home_team)

            elif match.away_score > match.home_score:
                winners.append(match.away_team)

        return winners

    def get_semi_final_losers(self):
        """
        Returns the semi-final losers.
        """

        losers = []

        for match in self.semi_finals:

            if match.status != "Completed":
                continue

            if match.home_score > match.away_score:
                losers.append(match.away_team)

            elif match.away_score > match.home_score:
                losers.append(match.home_team)

        return losers

    def generate_final(
        self,
        match_date,
        kickoff_time,
        venue
    ):
        """
        Generates the Final.
        """

        winners = self.get_semi_final_winners()

        if len(winners) != 2:

            print("Final cannot be generated yet.")
            return

        self.final = Match(
            fixture_id="FIN001",
            home_team=winners[0],
            away_team=winners[1],
            match_date=match_date,
            kickoff_time=kickoff_time,
            venue=venue,
            stage="Final"
        )

        self.tournament.add_match(self.final)

        print("\nFinal generated successfully.")

    def generate_third_place_match(
        self,
        match_date,
        kickoff_time,
        venue
    ):
        """
        Generates the Third Place Match.
        """

        losers = self.get_semi_final_losers()

        if len(losers) != 2:

            print("Third Place Match cannot be generated yet.")
            return

        self.third_place = Match(
            fixture_id="TP001",
            home_team=losers[0],
            away_team=losers[1],
            match_date=match_date,
            kickoff_time=kickoff_time,
            venue=venue,
            stage="Third Place"
        )

        self.tournament.add_match(self.third_place)

        print("\nThird Place Match generated successfully.")

    def display_final(self):

        print("\n========== FINAL ==========")

        if self.final:

            print(self.final)

        else:

            print("Final has not been generated.")

    def display_third_place_match(self):

        print("\n========== THIRD PLACE MATCH ==========")

        if self.third_place:

            print(self.third_place)

        else:

            print("Third Place Match has not been generated.")
