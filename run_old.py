from models.user import User
from flask import Flask, render_template, redirect, url_for
from extensions import db

app = Flask(__name__)

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

app.config["SECRET_KEY"] = "afit-football-2026"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/teams")
def teams():

    departments = [

        {
            "name": "Aerospace Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Mechanical Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Civil Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Electrical Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Computer Science",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Cyber Security",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Information & Communication Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Automotive Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Mechatronics Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Metallurgical & Materials Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Physics with Electronics",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Statistics",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Chemistry",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "International Relations",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Business Administration & Economics",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        },

        {
            "name": "Telecomms Engineering",
            "captain": "TBA",
            "manager": "TBA",
            "players": 20
        }

    ]

    return render_template(
        "teams.html",
        departments=departments
    )


@app.route("/team/<department_name>")
def team_profile(department_name):

    players = []

    return render_template(
        "team_profile.html",
        department_name=department_name.replace("-", " ").title(),
        players=players
    )


@app.route("/player/<player_name>")
def player_profile(player_name):

    return render_template(
        "player_profile.html",
        player_name=player_name.replace("-", " ").title()
    )


@app.route("/fixtures")
def fixtures():

    return render_template("fixtures.html")


@app.route("/match-center")
def match_center():

    return render_template("match_center.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/standings")
def standings():
    return render_template("standings.html")


@app.route("/tournament")
def tournament_hub():
    return render_template("tournament_hub.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/bracket")
def bracket():
    return render_template("bracket.html")

# ==========================================
# ADMIN LOGIN
# ==========================================


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    return render_template("admin/login.html")

# ==========================================
# ADMIN DASHBOARD
# ==========================================


@app.route("/admin/dashboard")
def admin_dashboard():

    return render_template("admin/dashboard.html")

# ==========================================
# CREATE DATABASE
# ==========================================


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
