from src.tournament import Tournament
from src.player import Player
from src.match import Match

from src.services.data_loader import (
    load_teams,
    get_team_by_name
)

from src.services.fixture_manager import FixtureManager
from src.services.qualification_manager import QualificationManager
from src.services.knockout_manager import KnockoutManager


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
    # Fixture Manager
    # ==========================================

    fixture_manager = FixtureManager(tournament)

    # ==========================================
    # Load Teams
    # ==========================================

    teams = load_teams(tournament)

    qualification_manager = QualificationManager(tournament)

    aerospace = get_team_by_name(
        teams,
        "Aerospace Engineering"
    )

    mechanical = get_team_by_name(
        teams,
        "Mechanical Engineering"
    )

    knockout_manager = KnockoutManager(tournament)

    # ==========================================
    # Create Groups
    # ==========================================

    tournament.create_group("A")
    tournament.create_group("B")
    tournament.create_group("C")
    tournament.create_group("D")

    # ==========================================
    # Assign Teams
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

    # ==========================================
    # Get Group A
    # ==========================================

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
    # Create Fixture
    # ==========================================

    match1 = Match(
        fixture_id="FIX001",
        home_team=aerospace,
        away_team=mechanical,
        match_date="12 July 2026",
        kickoff_time="4:00 PM",
        venue="University Football Pitch",
        stage="Group Stage",
        group="A"
    )

    # ==========================================
    # Register Fixture
    # ==========================================

    fixture_manager.add_fixture(match1)

    # ==========================================
    # Edit Fixture
    # ==========================================

    fixture_manager.edit_fixture(
        fixture_id="FIX001",
        kickoff_time="5:00 PM",
        venue="AFIT Stadium"
    )

    # ==========================================
    # Tournament Information
    # ==========================================

    tournament.display_info()

    tournament.display_teams()

    tournament.display_groups()

    fixture_manager.display_fixtures()

    aerospace.display_players()

    # ==========================================
    # Match Before Result
    # ==========================================

    print("\n----- MATCH BEFORE RESULT -----")

    match1.display_match()

    # ==========================================
    # Record Result
    # ==========================================

    match1.record_result(2, 1)

    # ==========================================
    # Match Events
    # ==========================================

    match1.add_goal(
        scorer=joseph,
        assist=david,
        minute=18
    )

    match1.add_yellow_card(
        player=joseph,
        minute=41
    )

    match1.add_substitution(
        player_out=joseph,
        player_in=ahmed,
        minute=67
    )

    match1.add_goal(
        scorer=david,
        minute=74
    )

    match1.add_red_card(
        player=david,
        minute=88
    )

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

    # ==========================================
    # Qualified Teams
    # ==========================================

    qualification_manager.display_qualified_teams()

    print("\n----- KNOCKOUT STAGE -----")

    knockout_manager.create_quarter_final(
        fixture_id="QF001",
        home_team=aerospace,
        away_team=mechanical,
        match_date="20 July 2026",
        kickoff_time="4:00 PM",
        venue="AFIT Stadium"
    )

    knockout_manager.display_quarter_finals()

    # ==========================================
    # Demo Quarter Final Result
    # ==========================================

    qf = knockout_manager.quarter_finals[0]

    qf.record_result(3, 2)

    print("\n----- QUARTER FINAL RESULT -----")

    qf.display_match()

    knockout_manager.display_quarter_final_winners()

    # ==========================================
    # Generate Semi Finals
    # ==========================================

    knockout_manager.generate_semi_finals(
        match_date="24 July 2026",
        kickoff_time="4:00 PM",
        venue="AFIT Stadium"
    )

    knockout_manager.display_semi_finals()

    # ==========================================
    # Final & Third Place Demo
    # ==========================================

    knockout_manager.generate_final(
        match_date="28 July 2026",
        kickoff_time="4:00 PM",
        venue="AFIT Stadium"
    )

    knockout_manager.generate_third_place_match(
        match_date="28 July 2026",
        kickoff_time="12:00 PM",
        venue="AFIT Stadium"
    )

    knockout_manager.display_final()

    knockout_manager.display_third_place_match()


if __name__ == "__main__":
    main()
