from src.tournament import Tournament
from src.team import Team
from src.player import Player
from src.match import Match
from src.group import Group


def main():
    # Create Tournament
    tournament = Tournament(
        name="Final Year Inter-Departmental Tournament",
        year=2026,
        number_of_groups=4,
        teams_per_group=4
    )

    # Create Teams
    aerospace = Team(
        name="Aerospace Engineering",
        captain="Joseph",
        manager="Joseph"
    )

    mechanical = Team(
        name="Mechanical Engineering",
        captain="David",
        manager="Musa"
    )

    # Register Teams
    tournament.add_team(aerospace)
    tournament.add_team(mechanical)

    # Create Group A
    group_a = Group("A")

    # Assign Teams To Group A
    group_a.add_team(aerospace)
    group_a.add_team(mechanical)

    # Create Players
    joseph = Player(
        name="Joseph Saheed",
        jersey_number=7,
        position="Left Wing"
    )

    david = Player(
        name="David Musa",
        jersey_number=10,
        position="Striker"
    )

    # Add Players to Aerospace
    aerospace.add_player(joseph)
    aerospace.add_player(david)

    # Create Match
    match1 = Match(
        home_team=aerospace,
        away_team=mechanical,
        match_date="12 July 2026",
        kickoff_time="4:00 PM",
        venue="University Football Pitch",
        stage="Group Stage",
        group="A"
    )

    # Display Tournament Information
    tournament.display_info()

    # Display Teams
    tournament.display_teams()

    # Display Players
    aerospace.display_players()

    # Display Match Before Result
    print("\n----- MATCH BEFORE RESULT -----")
    match1.display_match()

    # Record Match Result
    match1.record_result(2, 1)

    # Display Match After Result
    print("\n----- MATCH AFTER RESULT -----")
    match1.display_match()

    # Display Team Statistics
    print("\n----- TEAM STATISTICS -----")

    aerospace.display_statistics()
    mechanical.display_statistics()

    # Display Group Table
    print("\n----- GROUP TABLE -----")

    group_a.display_table()


if __name__ == "__main__":
    main()
