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
      # try:
      #   # we will always refresh token regardless, because it reduces chance of stale token if user stays on page for > 1 hour and doesn't cost us anything in the quotq (i think)
      #   # user = auth.refreshUser(session['refreshToken'])
      #   # session['idToken'] = user['idToken']
      #   # session['refreshToken'] = user['refreshToken']
      # except:
      #   # if refresh token isn't working, i.e. user acct deleted, disabled, or major account info changed
      #   return redirect(url_for('logout'))
      return f(*args, **kwargs)
    else:
      return redirect(url_for('login'))
  return wrapper

@LoginRequired
@app.route("/inbox", methods=['GET', 'POST'])
def inbox():
  databaseWrapper = db.Database()
  if request.method == "GET":
    (messages, conversations) = databaseWrapper.getInbox(session['email'])
    return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages)
  elif request.method == "POST":
    databaseWrapper.replyToMessage(request.form.get('msgId'), session['email'], request.form.get('message'))

    (messages, conversations) = databaseWrapper.getInbox(session['email'])
    return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages)


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
        session['idToken'] = response['idToken']
        session['refreshToken'] = response['refreshToken']

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
      session['name'] = user.display_name
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
