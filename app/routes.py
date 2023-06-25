from flask import render_template
from datetime import datetime
from app import app, db
from app.models.models import (
    LobbyingReport,
    LobbyingReportStatus,
    LobbyingReportType,
    Grassroot,
    Beneficiary,
    Firm
)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/lobbying_reports")
def lobbying_reports():
    return render_template(
        "lobbying_reports.html",
        title="Lobbying Reports",
        lobbying_reports=LobbyingReport.query.all(),
        lobbying_report_status=LobbyingReportStatus,
        Lobbying_report_type=LobbyingReportType,
    )


@app.route("/lobbying_report/<int:id>")
def lobbying_report(id):
    report = LobbyingReport.query.get(id)
    return render_template(
        "lobbying_report.html", title="Lobbying Report", report=report
    )


@app.route("/grassroots")
def grassroots():
    return render_template(
        "grassroots.html", title="Grassroots", grassroots=Grassroot.query.all()
    )

@app.route("/beneficiaries")
def beneficiaries():
    return render_template(
        "beneficiaries.html", title="beneficiaries", beneficiaries=Beneficiary.query.all()
    )

@app.route("/firms")
def firms():
    return render_template(
        "firms.html", title="Firms", firms=Firm.query.all()
    )

