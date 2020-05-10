from app import app
from flask import render_template, request, session, redirect, url_for, session

@app.route("/", methods=['GET', 'POST'])
def index():
  return render_template('index.html', title="Home")
