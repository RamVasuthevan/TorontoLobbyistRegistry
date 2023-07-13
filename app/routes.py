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
    Meeting,
    PublicOfficeHolder,
    Lobbyist,
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
        beneficiaries=Beneficiary.query.order_by(
            Beneficiary.name, Beneficiary.trade_name
        ).all(),
    )


@app.route("/beneficiary/<int:id>")
def beneficiary(id):
    beneficiary = Beneficiary.query.get(id)
    return render_template(
        "beneficiary.html", title="Beneficiary", beneficiary=beneficiary
    )


@app.route("/firms")
def firms():
    return render_template(
        "firms.html",
        title="firms",
        firms=Firm.query.order_by(Firm.name, Firm.trade_name).all(),
    )


@app.route("/firm/<int:id>")
def firm(id):
    firm = Firm.query.get(id)
    return render_template("firm.html", title="Firm", firm=firm)


@app.route("/privatefunding")
def privatefundings():
    return render_template(
        "privatefundings.html",
        title="Private Funding",
        private_fundings=PrivateFunding.query.order_by(PrivateFunding.funding).all(),
    )


@app.route("/governmentfunding")
def governmentfundings():
    return render_template(
        "governmentfundings.html",
        title="Government Funding",
        governmentfundings=GovernmentFunding.query.order_by(
            GovernmentFunding.government_name, GovernmentFunding.program
        ).all(),
    )


@app.route("/publicofficeholders")
def publicofficeholders():
    return render_template(
        "public_office_holders.html",
        title="Public Office Holders",
        publicofficeholders=PublicOfficeHolder.query.order_by(
            PublicOfficeHolder.type, PublicOfficeHolder.office, PublicOfficeHolder.name
        ).all(),
    )


@app.route("/lobbyists")
def lobbyists():
    return render_template(
        "lobbyists.html",
        title="Lobbyists",
        lobbyists=Lobbyist.query.all(),
    )


@app.route("/lobbyist/<int:id>")
def lobbyist(id):
    lobbyist = Lobbyist.query.get(id)
    lobbying_reports = (
        LobbyingReport.query.join(Meeting).join(Lobbyist, Lobbyist.id == id).all()
    )
    return render_template(
        "lobbyist.html",
        title="Lobbyist",
        lobbyist=lobbyist,
        lobbying_reports=lobbying_reports,
    )
