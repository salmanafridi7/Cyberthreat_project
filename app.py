from flask import Flask, render_template, request  #importing flask
from models import db, ThreatIntel, ThreatCategory #importing DB models

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///threatintel.db'

db.init_app(app)


# for home page
@app.route("/")
def home():

    threats = ThreatIntel.query.all()

    total_threats = ThreatIntel.query.count()

    high_severity = ThreatIntel.query.filter_by(
        severity="High"
    ).count()

    total_categories = ThreatCategory.query.count()

    total_sources = db.session.query(
        ThreatIntel.source
    ).distinct().count()

    return render_template(
        "index.html",
        threats=threats,
        total_threats=total_threats,
        high_severity=high_severity,
        total_categories=total_categories,
        total_sources=total_sources
    )


# for all the threats page
@app.route("/threats")
def threats():

    search = request.args.get("search")

    if search:

        all_threats = ThreatIntel.query.filter(
            ThreatIntel.threat_name.contains(search)
        ).all()

    else:

        all_threats = ThreatIntel.query.all()

    return render_template(
        "threats.html",
        threats=all_threats,
        search=search
    )


# individual threat page
@app.route("/threat/<int:id>")
def threat_detail(id):

    selected_threat = ThreatIntel.query.get_or_404(id)

    return render_template(
        "threat_detail.html",
        threat=selected_threat
    )


# for the compare page
@app.route("/compare")
def compare():

    categories = ThreatCategory.query.all()

    total_threats = ThreatIntel.query.count()

    category_info = []

    for category in categories:

        threat_count = len(category.threats)

        percentage = round((threat_count / total_threats) * 100, 2)

        sample_threats = category.threats[:3]

        if category.category_name == "Malware":

            description = (
                "Malware threats include malicious software "
                "such as viruses, ransomware, spyware, "
                "and trojans."
            )

        elif category.category_name == "Phishing":

            description = (
                "Phishing threats attempt to steal sensitive "
                "information using fake websites, emails, "
                "or login pages."
            )

        else:

            description = (
                "Suspicious activity includes unknown or "
                "potentially dangerous behaviour detected "
                "during monitoring."
            )

        category_info.append({

            "name": category.category_name,
            "count": threat_count,
            "percentage": percentage,
            "description": description,
            "samples": sample_threats

        })

    return render_template(
        "compare.html",
        categories=category_info,
        total_threats=total_threats
    )


# about the page
@app.route("/about")
def about():

    return render_template("about.html")


# CUSTOM 404 PAGE
@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


# CREATE DATABASE TABLES
with app.app_context():

    db.create_all()


# RUN APPLICATION
if __name__ == "__main__":

    app.run(debug=True)