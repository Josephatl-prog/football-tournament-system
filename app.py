from src.tournament import Tournament
from src.player import Player
from src.match import Match

from src.services.data_loader import (
    load_teams,
    get_team_by_name
)


def main():

    # ==========================================
    # Create Tournament
    # ==========================================

    tournament = Tournament(
        name="Final Year Inter-Departmental Tournament",
        year=2026,
        number_of_groups=4,
        teams_per_group=4
    )

    # ==========================================
    # Load Teams
    # ==========================================

    teams = load_teams(tournament)

    aerospace = get_team_by_name(
        teams,
        "Aerospace Engineering"
    )

    mechanical = get_team_by_name(
        teams,
        "Mechanical Engineering"
    )

    # ==========================================
    # Create Groups
    # ==========================================

    tournament.create_group("A")
    tournament.create_group("B")
    tournament.create_group("C")
    tournament.create_group("D")

    # ==========================================
    # Assign Teams to Groups
    # ==========================================

    # Group A
    tournament.assign_team_to_group("AER", "A")
    tournament.assign_team_to_group("AUT", "A")
    tournament.assign_team_to_group("CSC", "A")
    tournament.assign_team_to_group("MEC", "A")

    # Group B
    tournament.assign_team_to_group("EEE", "B")
    tournament.assign_team_to_group("ICE", "B")
    tournament.assign_team_to_group("CYB", "B")
    tournament.assign_team_to_group("TEL", "B")

    # Group C
    tournament.assign_team_to_group("CIV", "C")
    tournament.assign_team_to_group("MTR", "C")
    tournament.assign_team_to_group("MME", "C")
    tournament.assign_team_to_group("PHE", "C")

    # Group D
    tournament.assign_team_to_group("CHE", "D")
    tournament.assign_team_to_group("STA", "D")
    tournament.assign_team_to_group("IRS", "D")
    tournament.assign_team_to_group("BAE", "D")

    # Get Group A
    group_a = tournament.get_group("A")

    # ==========================================
    # Create Players
    # ==========================================

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

    ahmed = Player(
        name="Ahmed Ibrahim",
        jersey_number=17,
        position="Right Wing"
    )

    # ==========================================
    # Register Players
    # ==========================================

    aerospace.add_player(joseph)
    aerospace.add_player(david)
    aerospace.add_player(ahmed)

    # ==========================================
    # Create Match
    # ==========================================

    match1 = Match(
        home_team=aerospace,
        away_team=mechanical,
        match_date="12 July 2026",
        kickoff_time="4:00 PM",
        venue="University Football Pitch",
        stage="Group Stage",
        group="A"
    )

    # ==========================================
    # Add Match to Tournament
    # ==========================================

    tournament.add_match(match1)

    # ==========================================
    # Tournament Information
    # ==========================================

    tournament.display_info()

    tournament.display_teams()

    tournament.display_groups()

    tournament.display_matches()

    aerospace.display_players()

    # ==========================================
    # Match Before Result
    # ==========================================

    print("\n----- MATCH BEFORE RESULT -----")

    match1.display_match()

    # ==========================================
    # Record Match Result
    # ==========================================

    match1.record_result(2, 1)

    # ==========================================
    # Match Events
    # ==========================================

    # Goal
    match1.add_goal(
        scorer=joseph,
        assist=david,
        minute=18
    )

    # Yellow Card
    match1.add_yellow_card(
        player=joseph,
        minute=41
    )

    # Substitution
    match1.add_substitution(
        player_out=joseph,
        player_in=ahmed,
        minute=67
    )

    # Goal
    match1.add_goal(
        scorer=david,
        minute=74
    )

    # Red Card
    match1.add_red_card(
        player=david,
        minute=88
    )

    # Player of the Match
    match1.set_player_of_the_match(
        joseph
    )

    # ==========================================
    # Match After Result
    # ==========================================

    print("\n----- MATCH AFTER RESULT -----")

    match1.display_match()

    # ==========================================
    # Team Statistics
    # ==========================================

    print("\n----- TEAM STATISTICS -----")

    aerospace.display_statistics()
    mechanical.display_statistics()

    # ==========================================
    # Player Statistics
    # ==========================================

    print("\n----- PLAYER STATISTICS -----")

    joseph.display_statistics()
    david.display_statistics()
    ahmed.display_statistics()

    # ==========================================
    # Group Table
    # ==========================================

    print("\n----- GROUP TABLE -----")

    group_a.display_table()


if __name__ == "__main__":
    main()
