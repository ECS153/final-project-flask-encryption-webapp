from app import app
import requests
import firebase_admin
from flask import render_template, request, session, redirect, url_for, session
import app.database as db
import app.auth as auth

# LOGIN AND SIGN UP
@app.route("/", methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    if 'userId' in session:
      print("You are actually logged in")
      # return redirect(url_for('login')) # FIXME: CHANGE TO INBOX
    else:
      return render_template('index.html', title="Login/Sign Up!")

  if request.method == "POST":
      email = request.form.get("email")
      password = request.form.get("password")
      response = auth.loginUser(email, password)

      if response['userId'] and response['idToken']:
        session['userId'] = response['userId']
        session['idToken'] = response['idToken']
        session['refreshToken'] = response['refreshToken']

        return redirect(url_for('login')) # FIXME: CHANGE TO INBOX
      else:
        errorMessage = "Either your username or password is incorrect! Please try again"
        return render_template('login.html', errorMessage=errorMessage)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
  email = None
  errorMessage = ""
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    authWrapper = auth.Auth()
    databaseWrapper = db.Database()

    try:
      authWrapper.createUser(name, email, password)
      user = firebase_admin.auth.get_user_by_email(email)
      databaseWrapper.createUser(user=user)

      session['userId'] = user.uid
      session['name'] = user.display_name
      session['email'] = user.email

      return redirect(url_for('login')) # FIXME: CHANGE TO INBOX
    except requests.exceptions.HTTPError as err:
      errorDict = ast.literal_eval(err.strerror)
      errorMessage = errorDict["error"]["message"]
    except ValueError as err:
      errorMessage=err
    except firebase_admin._auth_utils.EmailAlreadyExistsError as err:
      errorMessage = err
  return render_template('signup.html', errorMessage=errorMessage)
