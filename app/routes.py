from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from app import app, db
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', users=users)
