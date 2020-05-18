from firebase_admin import auth
import pyrebase

config = {
  "apiKey": "AIzaSyBruM8GzdWDOdjC_ubpEPaWgUDZVJp72xI",
  "authDomain": "ecs153.firebaseapp.com",
  "databaseURL": "https://ecs153.firebaseio.com",
  "storageBucket": "ecs153.appspot.com",
  "serviceAccount": "./app/config/serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)


class Auth:
  auth = firebase.auth()

  def createUser(self, name, email, password):
    """ Creates a user in the Firebase authentication table """
    user = auth.create_user(
      display_name=name,
      email=email,
      password=password
    )
    return user

  def loginUser(self, email, password):
    """ Logs a user in with a given username and password. Returns the response object. """
    response = {"success": False, "message": None, "userId": None, "idToken": None, "refreshToken": None, "email": None}

    try:
      user = self.auth.sign_in_with_email_and_password(email, password)
      user = self.auth.refresh(user['refreshToken'])
      userId = user['userId']
      idToken = user['idToken']
      refreshToken = user['refreshToken']

      response["success"] = True
      response["message"] = "Successfully authenticated."
      response['userId'] = userId
      response['idToken'] = idToken
      response['refreshToken'] = refreshToken
      response['email'] = email
    except:
      response["message"] = "Failed to authenticate. Either username or password is incorrect."
    return response
