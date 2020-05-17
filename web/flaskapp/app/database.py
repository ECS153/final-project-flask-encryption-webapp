import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore


class Database:
  cred = credentials.Certificate('./app/config/serviceAccountKey.json')
  default_app = firebase_admin.initialize_app(cred)

  def createUser(self, user):
    """ Creates a new user in the 'users' table in firestore. User is a firebase admin user object. """
    db = firestore.client()
    doc_ref = db.collection('users').document(user.email)
    doc_ref.set({
      'userId': user.uid,
      'name': user.display_name,
      'email': user.email,
      'messages': []
    })
