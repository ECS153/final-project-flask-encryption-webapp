from app import app
import requests
import ast
import firebase_admin
from functools import wraps
from flask import render_template, request, session, redirect, url_for, session
import app.database as db
import app.auth as auth
import app.encryption as encrypt

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
  errorMessage = request.args.get('errorMessage')

  if errorMessage == None:
    errorMessage = ""

  if request.method == "GET":
    (messages, conversations) = databaseWrapper.GetInbox(session['email'], session['privateKey'])

    for messageId, messageObj in messages.items():
      for message in messageObj['messages']:
        encryptedMessage = message['messageContents'][session['email']]
        decryptedMessage = encrypt.Decrypt(session['privateKey'], encryptedMessage)
        message['messageContents'] = decryptedMessage

    return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages, errorMessage=errorMessage)
  elif request.method == "POST":
    if request.form.get('formType') == "reply":
      plaintextMessage = request.form.get('message')
      publicKey = databaseWrapper.GetPublicKeyForUser(request.form.get('to'))

      ciphertextSender = encrypt.Encrypt(session['publicKey'], plaintextMessage)
      ciphertextTo = encrypt.Encrypt(publicKey, plaintextMessage)

      databaseWrapper.ReplyToMessage(request.form.get('msgId'), request.form.get('to'), session['email'], ciphertextSender, ciphertextTo)
      (messages, conversations) = databaseWrapper.GetInbox(session['email'], session['privateKey'])
    elif request.form.get('formType') == "newMessage":
      plaintextMessage = request.form.get('message')
      publicKey = databaseWrapper.GetPublicKeyForUser(request.form.get('to'))

      if not publicKey:
        errorMessage = "That account does not exist. Please check the email and try again."
        return redirect(url_for('inbox', errorMessage=errorMessage))

      ciphertextSender = encrypt.Encrypt(session['publicKey'], plaintextMessage)
      ciphertextTo = encrypt.Encrypt(publicKey, plaintextMessage)

      errorMessage = databaseWrapper.CreateMessage(request.form.get('to'), session['email'], ciphertextSender, ciphertextTo)
      (messages, conversations) = databaseWrapper.GetInbox(session['email'], session['privateKey'])
    return redirect(url_for('inbox', errorMessage=errorMessage))

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
      response = authWrapper.LoginUser(email, password)

      if response['userId'] and response['idToken']:
        session['userId'] = response['userId']
        session['email'] = response['email']
        session['publicKey'] = response['publicKey']
        session['privateKey'] = response['privateKey']

        return redirect(url_for('inbox'))
      else:
        errorMessage = "Either your username or password is incorrect! Please try again"
        return render_template('index.html', errorMessage=errorMessage)


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
      authWrapper.CreateUser(name, email, password)
      user = firebase_admin.auth.get_user_by_email(email)
      publicKey, privateKey = databaseWrapper.CreateUser(user=user)

      session['userId'] = user.uid
      session['email'] = user.email
      session['publicKey'] = publicKey
      session['privateKey'] = privateKey


      return redirect(url_for('inbox'))
    except requests.exceptions.HTTPError as err:
      errorDict = ast.literal_eval(err.strerror)
      errorMessage = errorDict["error"]["message"]
    except ValueError as err:
      errorMessage=err
    except firebase_admin._auth_utils.EmailAlreadyExistsError as err:
      errorMessage = err
    except firebase_admin.exceptions.InvalidArgumentError as err:
      errorMessage = err
  return render_template('signup.html', errorMessage=errorMessage)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  session.clear()
  return redirect(url_for('login'))
