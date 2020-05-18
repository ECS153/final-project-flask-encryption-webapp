from app import app
import requests
import firebase_admin
from flask import render_template, request, session, redirect, url_for, session
import app.database as db
import app.auth as auth

# @LoginRequired  # FIXME: uncomment
@app.route("/inbox", methods=['GET', 'POST'])
def inbox():
  databaseWrapper = db.Database()
  (messages, conversations) = databaseWrapper.getInbox('nastern@ucdavis.edu')

  return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages)

# LOGIN AND SIGN UP
@app.route("/", methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    if 'userId' in session:
      # databaseWrapper = db.Database()
      # .strftime("%m/%d/%Y, %H:%M:%S")
      # databaseWrapper.createMessage('nastern2@ucdavis.edu', 'nastern@ucdavis.edu', 'Hello, world!')
      # databaseWrapper.replyToMessage('7hEWOxuSxWNFTxFlI60E','nastern2@ucdavis.edu', 'Hey, world!')
      # print(databaseWrapper.getInbox('nastern@ucdavis.edu'))

      return redirect(url_for('inbox'))
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

      return redirect(url_for('inbox'))
    except requests.exceptions.HTTPError as err:
      errorDict = ast.literal_eval(err.strerror)
      errorMessage = errorDict["error"]["message"]
    except ValueError as err:
      errorMessage=err
    except firebase_admin._auth_utils.EmailAlreadyExistsError as err:
      errorMessage = err
  return render_template('signup.html', errorMessage=errorMessage)
