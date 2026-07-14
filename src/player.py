class Player:
    """
    Represents a football player.
    """

    def __init__(self, name, jersey_number, position):
        self.name = name
        self.jersey_number = jersey_number
        self.position = position

        # Team Information
        self.team = None
        self.photo = None
        self.status = "Active"

        # Tournament Statistics
        self.matches_played = 0
        self.minutes_played = 0

        self.goals = 0
        self.assists = 0

        self.yellow_cards = 0
        self.red_cards = 0

        self.clean_sheets = 0

        self.player_of_the_match_awards = 0

    def display_statistics(self):
        """
        Displays the player's tournament statistics.
        """

        print(f"\nPlayer Statistics: {self.name}")
        print(f"Team: {self.team}")
        print(f"Position: {self.position}")
        print(f"Matches Played: {self.matches_played}")
        print(f"Minutes Played: {self.minutes_played}")
        print(f"Goals: {self.goals}")
        print(f"Assists: {self.assists}")
        print(f"Yellow Cards: {self.yellow_cards}")
        print(f"Red Cards: {self.red_cards}")
        print(f"Clean Sheets: {self.clean_sheets}")
        print(f"Player of the Match Awards: {self.player_of_the_match_awards}")

    def __str__(self):
        return f"#{self.jersey_number} {self.name} ({self.position})"
