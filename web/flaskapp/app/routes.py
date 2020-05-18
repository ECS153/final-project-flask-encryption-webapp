from app import app
import requests
import firebase_admin
from functools import wraps
from flask import render_template, request, session, redirect, url_for, session
import app.database as db
import app.auth as auth

def LoginRequired(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if 'userId' in session:
      return f(*args, **kwargs)
    else:
      return redirect(url_for('login'))
  return wrapper

@app.route("/inbox", methods=['GET', 'POST'])
@LoginRequired
def inbox():
  databaseWrapper = db.Database()
  errorMessage = ""
  if request.method == "GET":
    (messages, conversations) = databaseWrapper.getInbox(session['email'])
    return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages)
  elif request.method == "POST":
    if request.form.get('formType') == "reply":
      databaseWrapper.replyToMessage(request.form.get('msgId'), session['email'], request.form.get('message'))

      (messages, conversations) = databaseWrapper.getInbox(session['email'])
    elif request.form.get('formType') == "newMessage":
      errorMessage = databaseWrapper.createMessage(request.form.get('to'), session['email'], request.form.get('message'))

      (messages, conversations) = databaseWrapper.getInbox(session['email'])
    return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages, errorMessage=errorMessage)


# LOGIN AND SIGN UP
@app.route("/", methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    if 'userId' in session:
      return redirect(url_for('inbox'))
    else:
      return render_template('index.html', title="Login/Sign Up!")

  if request.method == "POST":
      authWrapper = auth.Auth()

      email = request.form.get("email")
      password = request.form.get("password")
      response = authWrapper.loginUser(email, password)

      if response['userId'] and response['idToken']:
        session['userId'] = response['userId']
        session['email'] = response['email']

        return redirect(url_for('inbox'))
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
      session['email'] = user.email

      return redirect(url_for('inbox'))
    except requests.exceptions.HTTPError as err:
      errorDict = ast.literal_eval(err.strerror)
      errorMessage = errorDict["error"]["message"]
    except ValueError as err:
      errorMessage=err
    except firebase_admin._auth_utils.EmailAlreadyExistsError as err:
      errorMessage = err
  return render_template('signup.html', errorMessage=errorMessage)

@app.route("/logout", methods=['GET', 'POST'])
@LoginRequired
def logout():
  session.clear()
  return redirect(url_for('login'))
