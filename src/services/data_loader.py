from src.team import Team


def load_teams(tournament):
    """
    Creates and registers all teams in the tournament.
    """

    teams = [

        Team("AER", "Aerospace Engineering", "TBD", "TBD"),
        Team("AUT", "Automotive Engineering", "TBD", "TBD"),
        Team("BAE", "Business Administration & Economics", "TBD", "TBD"),
        Team("CHE", "Chemistry", "TBD", "TBD"),
        Team("CIV", "Civil Engineering", "TBD", "TBD"),
        Team("CSC", "Computer Science", "TBD", "TBD"),
        Team("CYB", "Cyber Security", "TBD", "TBD"),
        Team("EEE", "Electrical/Electronic Engineering", "TBD", "TBD"),
        Team("ICE", "Information & Communication Engineering", "TBD", "TBD"),
        Team("IRS", "International Relations", "TBD", "TBD"),
        Team("MEC", "Mechanical Engineering", "TBD", "TBD"),
        Team("MTR", "Mechatronics Engineering", "TBD", "TBD"),
        Team("MME", "Metallurgical & Materials Engineering", "TBD", "TBD"),
        Team("PHE", "Physics with Electronics", "TBD", "TBD"),
        Team("STA", "Statistics", "TBD", "TBD"),
        Team("TEL", "Telecommunication Engineering", "TBD", "TBD")

    ]

    for team in teams:
        tournament.add_team(team)

    return teams


def get_team_by_name(teams, team_name):
    """
    Returns a team object by its name.
    """

    for team in teams:
        if team.name == team_name:
            return team

    return None
