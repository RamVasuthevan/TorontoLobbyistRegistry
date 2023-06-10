from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from app import app, db
from app.models import LobbyingReport

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/lobbying_reports')
def lobbying_reports():
    reports = LobbyingReport.query.all()
    return render_template('lobbying_reports.html', title='Lobbying Reports', reports=reports)

@app.route('/lobbying_report/<int:id>')
def lobbying_report(id):
    report = LobbyingReport.query.get(id)
    return render_template('lobbying_report.html', title='Lobbying Report', report=report)
