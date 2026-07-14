from src.tournament import Tournament
from src.player import Player
from src.match import Match

from src.services.data_loader import (
    load_teams,
    get_team_by_name
)


def main():

    # Create Tournament
    tournament = Tournament(
        name="Final Year Inter-Departmental Tournament",
        year=2026,
        number_of_groups=4,
        teams_per_group=4
    )

    # Load Teams
    teams = load_teams(tournament)

    # Retrieve Teams
    aerospace = get_team_by_name(
        teams,
        "Aerospace Engineering"
    )

    mechanical = get_team_by_name(
        teams,
        "Mechanical Engineering"
    )

    # Create Group A
    tournament.create_group("A")

    # Assign Teams to Group A
    tournament.assign_team_to_group("AER", "A")
    tournament.assign_team_to_group("MEC", "A")

    # Get Group A
    group_a = tournament.get_group("A")

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

    # Display Registered Teams
    tournament.display_teams()

    # Display Tournament Groups
    tournament.display_groups()

    # Display Players
    aerospace.display_players()

    # Match Before Result
    print("\n----- MATCH BEFORE RESULT -----")
    match1.display_match()

    # Record Match Result
    match1.record_result(2, 1)

    # Record Goals
    match1.add_goal(
        scorer=joseph,
        assist=david,
        minute=18
    )

    match1.add_goal(
        scorer=david,
        minute=74
    )

    # Match After Result
    print("\n----- MATCH AFTER RESULT -----")
    match1.display_match()

    # Team Statistics
    print("\n----- TEAM STATISTICS -----")
    aerospace.display_statistics()
    mechanical.display_statistics()

    # Player Statistics
    print("\n----- PLAYER STATISTICS -----")
    joseph.display_statistics()
    david.display_statistics()

    # Group Table
    print("\n----- GROUP TABLE -----")
    group_a.display_table()


if __name__ == "__main__":
    main()
