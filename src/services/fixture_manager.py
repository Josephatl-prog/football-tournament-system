class FixtureManager:
    """
    Manages tournament fixtures.
    """

    def __init__(self, tournament):

        self.tournament = tournament

    def add_fixture(self, match):

        self.tournament.add_match(match)

    def display_fixtures(self):

        print("\n========== TOURNAMENT FIXTURES ==========")

        if not self.tournament.matches:

            print("No fixtures available.")
            return

        for fixture in self.tournament.matches:

            print(fixture)

    def get_fixture(self, fixture_id):

        for fixture in self.tournament.matches:

            if fixture.fixture_id == fixture_id:

                return fixture

        return None

    def delete_fixture(self, fixture_id):

        fixture = self.get_fixture(fixture_id)

        if fixture:

            self.tournament.matches.remove(fixture)

            print(f"{fixture_id} deleted.")

        else:

            print("Fixture not found.")

    def edit_fixture(
        self,
        fixture_id,
        match_date=None,
        kickoff_time=None,
        venue=None,
        stage=None,
        group=None
    ):
        """
        Updates a fixture's details.
        """

        fixture = self.get_fixture(fixture_id)

        if not fixture:
            print("Fixture not found.")
            return

        if match_date:
            fixture.match_date = match_date

        if kickoff_time:
            fixture.kickoff_time = kickoff_time

        if venue:
            fixture.venue = venue

        if stage:
            fixture.stage = stage

        if group:
            fixture.group = group

        print(f"{fixture_id} updated successfully.")
