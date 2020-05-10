from app import app
from flask import render_template, request, session, redirect, url_for, session
import app.database as db

@app.route("/", methods=['GET', 'POST'])
def index():
  database = db.Database()
  return render_template('index.html', title="Home")
