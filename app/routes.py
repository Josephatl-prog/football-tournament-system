from flask import app, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required

from extensions import db
from sqlalchemy import func, case

from models.user import User
from models.team import Team
from models.player import Player
from models.fixture import Fixture
from models.group import Group
from models.match_event import MatchEvent
from models.lineup import Lineup


def register_routes(app):

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/fixtures")
    def fixtures():

        fixtures = Fixture.query.filter_by(
            status="Upcoming"
        ).order_by(
            Fixture.id.asc()
        ).all()

        return render_template(
            "fixtures.html",
            fixtures=fixtures
        )

    @app.route("/results")
    def results():
        return render_template("results.html")

    @app.route("/standings")
    def standings():

        groups = Group.query.order_by(
            Group.id
        ).all()

        return render_template(
            "standings.html",
            groups=groups
        )

    @app.route("/statistics")
    def statistics():

        # ==========================================
        # QUICK TOURNAMENT STATISTICS
        # ==========================================

        played_fixtures = Fixture.query.filter_by(
            status="Played"
        ).all()

        total_matches = len(played_fixtures)

        total_goals = sum(
            (fixture.home_score or 0) +
            (fixture.away_score or 0)
            for fixture in played_fixtures
        )

        total_assists = MatchEvent.query.filter(
            MatchEvent.event_type == "goal",
            MatchEvent.assist_player_id.isnot(None)
        ).count()

        total_yellow_cards = MatchEvent.query.filter_by(
            event_type="yellow_card"
        ).count()

        total_red_cards = MatchEvent.query.filter_by(
            event_type="red_card"
        ).count()

        # ==========================================
        # TOP GOAL SCORERS
        # ==========================================

        top_scorers = (
            db.session.query(
                Player,
                func.count(MatchEvent.id).label("goals")
            )
            .join(
                MatchEvent,
                MatchEvent.player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "goal"
            )
            .group_by(Player.id)
            .order_by(
                func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # TOP ASSISTS
        # ==========================================

        top_assists = (
            db.session.query(
                Player,
                func.count(MatchEvent.id).label("assists")
            )
            .join(
                MatchEvent,
                MatchEvent.assist_player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "goal",
                MatchEvent.assist_player_id.isnot(None)
            )
            .group_by(Player.id)
            .order_by(
                func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # DISCIPLINE
        # ==========================================

        discipline = (
            db.session.query(
                Player,

                func.sum(
                    case(
                        (MatchEvent.event_type == "yellow_card",
                            1
                         ),
                        else_=0
                    )
                ).label("yellow_cards"),

                func.sum(
                    case(
                        (MatchEvent.event_type == "red_card",
                            1
                         ),
                        else_=0
                    )
                ).label("red_cards")
            )
            .join(
                MatchEvent,
                MatchEvent.player_id == Player.id
            )
            .filter(
                MatchEvent.event_type.in_(
                    ["yellow_card", "red_card"]
                )
            )
            .group_by(Player.id)
            .order_by(
                func.sum(
                    case(
                        (MatchEvent.event_type == "yellow_card",
                            1
                         ),
                        else_=0
                    )
                ).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # TEAM STATISTICS
        # ==========================================

        teams = Team.query.all()

        # Highest scoring team
        highest_scoring_team = max(
            teams,
            key=lambda team: team.goals_for or 0,
            default=None
        )

        # Best defence
        best_defence_team = min(
            teams,
            key=lambda team: team.goals_against or 0,
            default=None
        )

        # Most wins
        most_wins_team = max(
            teams,
            key=lambda team: team.won or 0,
            default=None
        )

        # ==========================================
        # CLEAN SHEETS
        # ==========================================

        clean_sheets = {}

        for team in teams:

            count = 0

            for fixture in played_fixtures:

                # Team played at home and kept a clean sheet
                if (
                    fixture.home_team_id == team.id
                    and (fixture.away_score or 0) == 0
                ):
                    count += 1

                # Team played away and kept a clean sheet
                elif (
                    fixture.away_team_id == team.id
                    and (fixture.home_score or 0) == 0
                ):
                    count += 1

            clean_sheets[team.id] = count

        # ==========================================
        # GOALKEEPERS
        # ==========================================

        goalkeepers = []

        for team in teams:

            # Find goalkeeper(s) belonging to this team
            team_goalkeepers = [
                player
                for player in team.players_list
                if (player.position or "").strip().lower()
                in ["goalkeeper", "gk"]
            ]

            for goalkeeper in team_goalkeepers:

                goalkeepers.append({
                    "player": goalkeeper,
                    "team": team,
                    "clean_sheets": clean_sheets.get(
                        team.id,
                        0
                    )
                })

        # Sort highest clean sheets first
        goalkeepers.sort(
            key=lambda item: item["clean_sheets"],
            reverse=True
        )

        # ==========================================
        # TEAM WITH MOST CLEAN SHEETS
        # ==========================================

        most_clean_sheets_team = max(
            teams,
            key=lambda team: clean_sheets.get(
                team.id,
                0
            ),
            default=None
        )

        return render_template(
            "statistics.html",

            total_matches=total_matches,
            total_goals=total_goals,
            total_assists=total_assists,
            total_yellow_cards=total_yellow_cards,
            total_red_cards=total_red_cards,

            top_scorers=top_scorers,
            top_assists=top_assists,
            discipline=discipline,

            goalkeepers=goalkeepers,

            highest_scoring_team=highest_scoring_team,
            best_defence_team=best_defence_team,
            most_wins_team=most_wins_team,
            most_clean_sheets_team=most_clean_sheets_team,

            clean_sheets=clean_sheets
        )

    @app.route("/teams")
    def teams():
        return render_template("teams.html")

    @app.route("/tournament")
    def tournament_hub():
        return render_template("tournament_hub.html")

    @app.route("/bracket")
    def bracket():
        return render_template("bracket.html")

    @app.route("/match-center")
    def match_center():
        return render_template("match_center.html")

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():

        if request.method == "POST":

            email = request.form.get("email")

            password = request.form.get("password")

            admin = User.query.filter_by(email=email).first()

            if admin and admin.password == password:

                login_user(admin)

                flash("Welcome Admin!", "success")

                return redirect(url_for("admin_dashboard"))

            flash("Invalid email or password.", "danger")

        return render_template("admin/login.html")

    @app.route("/admin/dashboard")
    @login_required
    def admin_dashboard():
        return render_template("admin/dashboard.html")

    @app.route("/admin/manage-teams")
    @login_required
    def manage_teams():

        teams = Team.query.all()

        return render_template(
            "admin/manage_teams.html",
            teams=teams
        )

    @app.route("/admin/add-team", methods=["GET", "POST"])
    @login_required
    def add_team():

        if request.method == "POST":

            team = Team(
                name=request.form["name"],
                captain=request.form["captain"],
                manager=request.form["manager"],
                players=int(request.form["players"])
            )

            db.session.add(team)
            db.session.commit()

            return redirect(url_for("manage_teams"))

        return render_template("admin/add_team.html")

    @app.route("/admin/edit-team/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_team(id):

        team = Team.query.get_or_404(id)

        if request.method == "POST":

            team.name = request.form["name"]
            team.captain = request.form["captain"]
            team.manager = request.form["manager"]
            team.players = int(request.form["players"])

            db.session.commit()

            flash("Team updated successfully!", "success")

            return redirect(url_for("manage_teams"))

        return render_template(
            "admin/edit_team.html",
            team=team
        )

    @app.route("/admin/delete-team/<int:id>", methods=["POST"])
    @login_required
    def delete_team(id):

        team = Team.query.get_or_404(id)

        db.session.delete(team)

        db.session.commit()

        flash("Team deleted successfully!", "success")

        return redirect(url_for("manage_teams"))

    @app.route("/admin/manage-players")
    @login_required
    def manage_players():

        players = Player.query.all()

        return render_template(
            "admin/manage_players.html",
            players=players
        )

    @app.route("/admin/add-player", methods=["GET", "POST"])
    @login_required
    def add_player():

        teams = Team.query.all()

        if request.method == "POST":

            player = Player(

                full_name=request.form["full_name"],

                jersey_number=int(request.form["jersey_number"]),

                position=request.form["position"],

                team_id=int(request.form["team_id"]),

                status=request.form["status"]

            )

            db.session.add(player)

            db.session.commit()

            flash("Player added successfully!", "success")

            return redirect(url_for("manage_players"))

        return render_template(
            "admin/add_player.html",
            teams=teams
        )

    @app.route("/admin/edit-player/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_player(id):

        player = Player.query.get_or_404(id)

        teams = Team.query.all()

        if request.method == "POST":

            player.full_name = request.form["full_name"]

            player.jersey_number = int(request.form["jersey_number"])

            player.position = request.form["position"]

            player.team_id = int(request.form["team_id"])

            player.status = request.form["status"]

            db.session.commit()

            flash("Player updated successfully!", "success")

            return redirect(url_for("manage_players"))

        return render_template(
            "admin/edit_player.html",
            player=player,
            teams=teams
        )

    @app.route("/admin/delete-player/<int:id>", methods=["POST"])
    @login_required
    def delete_player(id):

        player = Player.query.get_or_404(id)

        db.session.delete(player)

        db.session.commit()

        flash("Player deleted successfully!", "success")

        return redirect(url_for("manage_players"))

    @app.route("/admin/manage-fixtures")
    @login_required
    def manage_fixtures():

        fixtures = Fixture.query.all()

        return render_template(
            "admin/manage_fixtures.html",
            fixtures=fixtures
        )

    @app.route("/admin/add-fixture", methods=["GET", "POST"])
    @login_required
    def add_fixture():

        teams = Team.query.all()

        if request.method == "POST":

            home_team = int(request.form["home_team_id"])
            away_team = int(request.form["away_team_id"])

            if home_team == away_team:

                flash("Home and Away teams cannot be the same.", "danger")

                return redirect(url_for("add_fixture"))

            fixture = Fixture(

                home_team_id=home_team,

                away_team_id=away_team,

                match_date=request.form["match_date"],

                kickoff_time=request.form["kickoff_time"],

                venue=request.form["venue"],

                stage=request.form["stage"],

                group=request.form["group"]

            )

            db.session.add(fixture)

            db.session.commit()

            flash("Fixture created successfully!", "success")

            return redirect(url_for("manage_fixtures"))

        return render_template(
            "admin/add_fixture.html",
            teams=teams
        )

    @app.route("/admin/edit-fixture/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_fixture(id):

        fixture = Fixture.query.get_or_404(id)

        teams = Team.query.all()

        if request.method == "POST":

            home_team = int(request.form["home_team_id"])
            away_team = int(request.form["away_team_id"])

            if home_team == away_team:

                flash("Home and Away teams cannot be the same.", "danger")
                return redirect(url_for("edit_fixture", id=id))

            fixture.home_team_id = home_team
            fixture.away_team_id = away_team
            fixture.match_date = request.form["match_date"]
            fixture.kickoff_time = request.form["kickoff_time"]
            fixture.venue = request.form["venue"]
            fixture.stage = request.form["stage"]
            fixture.group = request.form["group"]

            db.session.commit()

            flash("Fixture updated successfully!", "success")

            return redirect(url_for("manage_fixtures"))

        return render_template(
            "admin/edit_fixture.html",
            fixture=fixture,
            teams=teams
        )

    @app.route("/admin/delete-fixture/<int:id>", methods=["POST"])
    @login_required
    def delete_fixture(id):

        fixture = Fixture.query.get_or_404(id)

        db.session.delete(fixture)

        db.session.commit()

        flash("Fixture deleted successfully!", "success")

        return redirect(url_for("manage_fixtures"))

    @app.route("/admin/match-results")
    @login_required
    def record_match_results():

        fixtures = Fixture.query.filter_by(
            status="Upcoming"
        ).all()

        return render_template(
            "admin/record_match_results.html",
            fixtures=fixtures
        )

    @app.route("/admin/match-report/<int:id>", methods=["GET", "POST"])
    @login_required
    def match_report(id):

        fixture = Fixture.query.get_or_404(id)

        home_players = Player.query.filter_by(
            team_id=fixture.home_team_id
        ).all()

        away_players = Player.query.filter_by(
            team_id=fixture.away_team_id
        ).all()

        if request.method == "POST":

            # ==========================================
            # MATCH SCORE
            # ==========================================

            fixture.home_score = int(
                request.form.get("home_score", 0)
            )

            fixture.away_score = int(
                request.form.get("away_score", 0)
            )

            fixture.status = "Played"

            # ==========================================
            # GET TEAMS
            # ==========================================

            home_team = fixture.home_team
            away_team = fixture.away_team

            # ==========================================
            # TEAM STATISTICS
            # ==========================================

            home_team.played += 1
            away_team.played += 1

            # Goals

            home_team.goals_for += fixture.home_score
            home_team.goals_against += fixture.away_score

            away_team.goals_for += fixture.away_score
            away_team.goals_against += fixture.home_score

            # ==========================================
            # MATCH RESULT
            # ==========================================

            if fixture.home_score > fixture.away_score:

                home_team.won += 1
                away_team.lost += 1

                home_team.points += 3

            elif fixture.home_score < fixture.away_score:

                away_team.won += 1
                home_team.lost += 1

                away_team.points += 3

            else:

                home_team.drawn += 1
                away_team.drawn += 1

                home_team.points += 1
                away_team.points += 1

            # ==========================================
            # GOAL DIFFERENCE
            # ==========================================

            home_team.goal_difference = (
                home_team.goals_for -
                home_team.goals_against
            )

            away_team.goal_difference = (
                away_team.goals_for -
                away_team.goals_against
            )

            # ==========================================
            # SAVE GOAL EVENTS
            # ==========================================

            home_scorers = request.form.getlist(
                "home_goal_scorers[]"
            )

            home_minutes = request.form.getlist(
                "home_minutes[]"
            )

            for index, player_id in enumerate(home_scorers):

                if player_id:

                    minute = None
                    assist_player_id = None

                    if index < len(home_minutes):
                        if home_minutes[index]:
                            minute = int(home_minutes[index])

                    if index < len(request.form.getlist("home_assists[]")):
                        assist_id = request.form.getlist(
                            "home_assists[]"
                        )[index]

                        if assist_id:
                            assist_player_id = int(assist_id)

                    event = MatchEvent(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        event_type="goal",
                        minute=minute,
                        assist_player_id=assist_player_id
                    )

                    db.session.add(event)

            # ==========================================
            # AWAY GOAL EVENTS
            # ==========================================

            away_scorers = request.form.getlist(
                "away_goal_scorers[]"
            )

            away_minutes = request.form.getlist(
                "away_minutes[]"
            )

            for index, player_id in enumerate(away_scorers):

                if player_id:

                    minute = None
                    assist_player_id = None

                    if index < len(away_minutes):
                        if away_minutes[index]:
                            minute = int(away_minutes[index])

                    if index < len(request.form.getlist("away_assists[]")):
                        assist_id = request.form.getlist(
                            "away_assists[]"
                        )[index]

                        if assist_id:
                            assist_player_id = int(assist_id)

                    event = MatchEvent(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        event_type="goal",
                        minute=minute,
                        assist_player_id=assist_player_id
                    )

                    db.session.add(event)

            # ==========================================
            # HOME YELLOW CARDS
            # ==========================================

            home_yellow_cards = request.form.getlist(
                "home_yellow_cards[]"
            )

            for player_id in home_yellow_cards:

                if player_id:

                    event = MatchEvent(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        event_type="yellow_card"
                    )

                    db.session.add(event)

            # ==========================================
            # HOME RED CARDS
            # ==========================================

            home_red_cards = request.form.getlist(
                "home_red_cards[]"
            )

            for player_id in home_red_cards:

                if player_id:

                    event = MatchEvent(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        event_type="red_card"
                    )

                    db.session.add(event)

            # ==========================================
            # AWAY YELLOW CARDS
            # ==========================================

            away_yellow_cards = request.form.getlist(
                "away_yellow_cards[]"
            )

            for player_id in away_yellow_cards:

                if player_id:

                    event = MatchEvent(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        event_type="yellow_card"
                    )

                    db.session.add(event)

            # ==========================================
            # AWAY RED CARDS
            # ==========================================

            away_red_cards = request.form.getlist(
                "away_red_cards[]"
            )

            for player_id in away_red_cards:

                if player_id:

                    event = MatchEvent(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        event_type="red_card"
                    )

                    db.session.add(event)

            # ==========================================
            # PLAYER OF THE MATCH
            # ==========================================

            player_of_the_match = request.form.get(
                "player_of_the_match"
            )

            if player_of_the_match:

                event = MatchEvent(
                    fixture_id=fixture.id,
                    player_id=int(player_of_the_match),
                    event_type="player_of_the_match"
                )

                db.session.add(event)
            # ==========================================
            # SAVE EVERYTHING
            # ==========================================

            db.session.commit()

            flash(
                "Match report saved successfully!",
                "success"
            )

            return redirect(
                url_for("record_match_results")
            )

        # ==============================================
        # DISPLAY MATCH REPORT
        # ==============================================

        return render_template(
            "admin/match_report.html",
            fixture=fixture,
            home_players=home_players,
            away_players=away_players
        )

    @app.route("/admin/statistics")
    @login_required
    def view_statistics():

        # ==========================================
        # LEAGUE TABLE
        # ==========================================

        teams = Team.query.order_by(
            Team.points.desc(),
            Team.goal_difference.desc(),
            Team.goals_for.desc()
        ).all()

        # ==========================================
        # GENERAL TOURNAMENT STATISTICS
        # ==========================================

        total_teams = Team.query.count()

        played_fixtures = Fixture.query.filter_by(
            status="Played"
        ).all()

        total_matches = len(played_fixtures)

        # ==========================================
        # TOTAL GOALS
        # ==========================================

        total_goals = sum(
            (fixture.home_score or 0) +
            (fixture.away_score or 0)
            for fixture in played_fixtures
        )

        # ==========================================
        # AVERAGE GOALS
        # ==========================================

        if total_matches > 0:

            average_goals = round(
                total_goals / total_matches,
                2
            )

        else:

            average_goals = 0

        # ==========================================
        # TOP SCORERS
        # ==========================================

        top_scorers = (
            db.session.query(
                Player,
                db.func.count(MatchEvent.id).label("goals")
            )
            .join(
                MatchEvent,
                MatchEvent.player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "goal"
            )
            .group_by(
                Player.id
            )
            .order_by(
                db.func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # TOP ASSISTS
        # ==========================================

        top_assists = (
            db.session.query(
                Player,
                db.func.count(MatchEvent.id).label("assists")
            )
            .join(
                MatchEvent,
                MatchEvent.assist_player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "goal",
                MatchEvent.assist_player_id.isnot(None)
            )
            .group_by(
                Player.id
            )
            .order_by(
                db.func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # TOP YELLOW CARDS
        # ==========================================

        top_yellow_cards = (
            db.session.query(
                Player,
                db.func.count(MatchEvent.id).label("yellow_cards")
            )
            .join(
                MatchEvent,
                MatchEvent.player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "yellow_card"
            )
            .group_by(
                Player.id
            )
            .order_by(
                db.func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # TOP RED CARDS
        # ==========================================

        top_red_cards = (
            db.session.query(
                Player,
                db.func.count(MatchEvent.id).label("red_cards")
            )
            .join(
                MatchEvent,
                MatchEvent.player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "red_card"
            )
            .group_by(
                Player.id
            )
            .order_by(
                db.func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # PLAYER OF THE MATCH
        # ==========================================

        top_player_of_match = (
            db.session.query(
                Player,
                db.func.count(MatchEvent.id).label("awards")
            )
            .join(
                MatchEvent,
                MatchEvent.player_id == Player.id
            )
            .filter(
                MatchEvent.event_type == "player_of_the_match"
            )
            .group_by(
                Player.id
            )
            .order_by(
                db.func.count(MatchEvent.id).desc()
            )
            .limit(10)
            .all()
        )

        # ==========================================
        # COMPLETE PLAYER STATISTICS
        # ==========================================

        players = Player.query.all()

        player_statistics = []

        for player in players:

            goals = MatchEvent.query.filter_by(
                player_id=player.id,
                event_type="goal"
            ).count()

            assists = MatchEvent.query.filter_by(
                assist_player_id=player.id,
                event_type="goal"
            ).count()

            yellow_cards = MatchEvent.query.filter_by(
                player_id=player.id,
                event_type="yellow_card"
            ).count()

            red_cards = MatchEvent.query.filter_by(
                player_id=player.id,
                event_type="red_card"
            ).count()

            potm = MatchEvent.query.filter_by(
                player_id=player.id,
                event_type="player_of_the_match"
            ).count()

            player_statistics.append({
                "player": player,
                "goals": goals,
                "assists": assists,
                "yellow_cards": yellow_cards,
                "red_cards": red_cards,
                "potm": potm
            })

        # Sort by goals, then assists
        player_statistics.sort(
            key=lambda x: (
                x["goals"],
                x["assists"],
                x["potm"]
            ),
            reverse=True
        )
        # ==========================================
        # RECENT MATCH EVENTS
        # ==========================================

        events = (
            MatchEvent.query
            .order_by(
                MatchEvent.fixture_id.desc(),
                MatchEvent.minute.asc()
            )
            .limit(30)
            .all()
        )

        # ==========================================
        # PREPARE EVENT DISPLAY DATA
        # ==========================================

        match_events = []

        for event in events:

            fixture = Fixture.query.get(
                event.fixture_id
            )

            player = Player.query.get(
                event.player_id
            )

            assist_player = None

            if event.assist_player_id:

                assist_player = Player.query.get(
                    event.assist_player_id
                )

            if fixture and player:

                match_events.append({
                    "fixture": fixture,
                    "player": player,
                    "assist": assist_player,
                    "minute": event.minute,
                    "event_type": event.event_type
                })

        # ==========================================
        # DISPLAY STATISTICS PAGE
        # ==========================================

        return render_template(
            "admin/statistics.html",

            teams=teams,

            total_teams=total_teams,

            total_matches=total_matches,

            total_goals=total_goals,

            average_goals=average_goals,

            top_scorers=top_scorers,

            top_assists=top_assists,

            top_yellow_cards=top_yellow_cards,

            top_red_cards=top_red_cards,

            top_player_of_match=top_player_of_match,

            player_statistics=player_statistics,

            match_events=match_events
        )

    @app.route("/admin/group-draw", methods=["GET", "POST"])
    @login_required
    def group_draw():

        groups = Group.query.order_by(Group.id).all()

        teams = Team.query.order_by(Team.name).all()

        if request.method == "POST":

            # First, remove existing group assignments
            for team in teams:
                team.group_id = None

            # Process each group
            for group in groups:

                team_ids = request.form.getlist(
                    f"group_{group.id}"
                )

                # Maximum 4 teams per group
                if len(team_ids) != 4:

                    flash(
                        f"Group {group.name} cannot have more than 4 teams.",
                        "danger"
                    )

                    return redirect(
                        url_for("group_draw")
                    )

                for team_id in team_ids:

                    team = Team.query.get(int(team_id))

                    if team:
                        team.group_id = group.id

            # Make sure every team is assigned exactly once
            assigned_teams = Team.query.filter(
                Team.group_id.isnot(None)
            ).count()

            if assigned_teams != len(teams):

                db.session.rollback()

                flash(
                    "Every team must be assigned to a group before saving the draw.",
                    "danger"
                )

                return redirect(
                    url_for("group_draw")
                )

            db.session.commit()

            flash(
                "Group draw saved successfully!",
                "success"
            )

            return redirect(
                url_for("group_draw")
            )

        return render_template(
            "admin/group_draw.html",
            groups=groups,
            teams=teams
        )

    @app.route("/fixtures/<int:fixture_id>/lineup")
    def view_lineup(fixture_id):

        fixture = Fixture.query.get_or_404(fixture_id)

        # Lineup has not been published yet
        if not fixture.lineup_published:
            return render_template(
                "lineup.html",
                fixture=fixture,
                lineup_published=False,
                home_lineup=[],
                away_lineup=[],
                home_substitutes=[],
                away_substitutes=[]
            )

        # Get saved lineup records
        home_lineup = (
            Lineup.query
            .filter_by(
                fixture_id=fixture.id,
                team_id=fixture.home_team_id,
                is_starting=True
            )
            .all()
        )

        away_lineup = (
            Lineup.query
            .filter_by(
                fixture_id=fixture.id,
                team_id=fixture.away_team_id,
                is_starting=True
            )
            .all()
        )

        home_substitutes = (
            Lineup.query
            .filter_by(
                fixture_id=fixture.id,
                team_id=fixture.home_team_id,
                is_starting=False
            )
            .all()
        )

        away_substitutes = (
            Lineup.query
            .filter_by(
                fixture_id=fixture.id,
                team_id=fixture.away_team_id,
                is_starting=False
            )
            .all()
        )

        return render_template(
            "lineup.html",
            fixture=fixture,
            lineup_published=True,
            home_lineup=home_lineup,
            away_lineup=away_lineup,
            home_substitutes=home_substitutes,
            away_substitutes=away_substitutes
        )

    @app.route("/admin/manage-lineups")
    @login_required
    def manage_lineups():

        fixtures = Fixture.query.filter_by(
            status="Upcoming"
        ).order_by(
            Fixture.id.asc()
        ).all()

        return render_template(
            "admin/manage_lineups.html",
            fixtures=fixtures
        )

    @app.route(
        "/admin/fixtures/<int:fixture_id>/lineup",
        methods=["GET", "POST"]
    )
    def manage_lineup(fixture_id):

        fixture = Fixture.query.get_or_404(fixture_id)

        home_players = Player.query.filter_by(
            team_id=fixture.home_team_id
        ).all()

        away_players = Player.query.filter_by(
            team_id=fixture.away_team_id
        ).all()

        # ==========================================
        # SAVE & PUBLISH LINEUP
        # ==========================================

        if request.method == "POST":

            # Remove any previous lineup for this fixture
            Lineup.query.filter_by(
                fixture_id=fixture.id
            ).delete()

            # ==========================================
            # HOME TEAM STARTING XI
            # ==========================================

            home_positions = {
                "home_GK": "GK",

                "home_LB": "LB",
                "home_CB1": "CB",
                "home_CB2": "CB",
                "home_RB": "RB",

                "home_CM1": "CM",
                "home_CM2": "CM",
                "home_CM3": "CM",

                "home_LW": "LW",
                "home_ST": "ST",
                "home_RW": "RW"
            }

            for field_name, position in home_positions.items():

                player_id = request.form.get(field_name)

                if player_id:

                    lineup = Lineup(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        team_id=fixture.home_team_id,
                        position=position,
                        is_starting=True
                    )

                    db.session.add(lineup)

            # ==========================================
            # HOME SUBSTITUTES
            # ==========================================

            home_substitutes = request.form.getlist(
                "home_substitutes"
            )

            for player_id in home_substitutes:

                lineup = Lineup(
                    fixture_id=fixture.id,
                    player_id=int(player_id),
                    team_id=fixture.home_team_id,
                    position="SUB",
                    is_starting=False
                )

                db.session.add(lineup)

            # ==========================================
            # AWAY TEAM STARTING XI
            # ==========================================

            away_positions = {
                "away_GK": "GK",

                "away_LB": "LB",
                "away_CB1": "CB",
                "away_CB2": "CB",
                "away_RB": "RB",

                "away_CM1": "CM",
                "away_CM2": "CM",
                "away_CM3": "CM",

                "away_LW": "LW",
                "away_ST": "ST",
                "away_RW": "RW"
            }

            for field_name, position in away_positions.items():

                player_id = request.form.get(field_name)

                if player_id:

                    lineup = Lineup(
                        fixture_id=fixture.id,
                        player_id=int(player_id),
                        team_id=fixture.away_team_id,
                        position=position,
                        is_starting=True
                    )

                    db.session.add(lineup)

            # ==========================================
            # AWAY SUBSTITUTES
            # ==========================================

            away_substitutes = request.form.getlist(
                "away_substitutes"
            )

            for player_id in away_substitutes:

                lineup = Lineup(
                    fixture_id=fixture.id,
                    player_id=int(player_id),
                    team_id=fixture.away_team_id,
                    position="SUB",
                    is_starting=False
                )

                db.session.add(lineup)

            # ==========================================
            # PUBLISH
            # ==========================================

            fixture.lineup_published = True

            db.session.commit()

            return redirect(
                url_for(
                    "manage_lineups"
                )
            )

        # ==========================================
        # DISPLAY ADMIN LINEUP PAGE
        # ==========================================

        return render_template(
            "admin/lineup.html",
            fixture=fixture,
            home_players=home_players,
            away_players=away_players
        )
