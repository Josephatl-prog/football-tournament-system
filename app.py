from src.tournament import Tournament
from src.team import Team
from src.player import Player


def main():
    tournament = Tournament(
        name="Final Year Inter-Departmental Tournament",
        year=2026,
        number_of_groups=4,
        teams_per_group=4
    )

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

    tournament.add_team(aerospace)
    tournament.add_team(mechanical)

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

    aerospace.add_player(joseph)
    aerospace.add_player(david)

    tournament.display_info()
    tournament.display_teams()

    aerospace.display_players()


if __name__ == "__main__":
    main()
