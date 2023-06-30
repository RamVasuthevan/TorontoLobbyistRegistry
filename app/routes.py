from flask import render_template
from datetime import datetime
from app import app, db
from app.models.models import (
    LobbyingReport,
    LobbyingReportStatus,
    LobbyingReportType,
    Grassroot,
    Beneficiary,
    Firm,
    PrivateFunding,
    GovernmentFunding,
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
        lobbying_reports=LobbyingReport.query.all()
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
        "beneficiaries.html",
        title="beneficiaries",
        beneficiaries=Beneficiary.query.order_by(Beneficiary.name, Beneficiary.trade_name).all(),
    )


@app.route("/beneficiary/<int:id>")
def beneficiary(id):
    beneficiary = Beneficiary.query.get(id)
    return render_template(
        "beneficiary.html", title="Beneficiary", beneficiary=beneficiary
    )


@app.route("/firms")
def firms():
    return render_template("firms.html", title="Firms", firms=Firm.query.all())


@app.route("/privatefunding")
def privatefunding():
    return render_template(
        "privatefunding.html",
        title="Private Funding",
        privatefundings=PrivateFunding.query.all(),
    )


@app.route("/governmentfunding")
def governmentfunding():
    return render_template(
        "governmentfunding.html",
        title="Government Funding",
        governmentfundings=GovernmentFunding.query.all(),
    )


