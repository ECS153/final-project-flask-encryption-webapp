from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore


class Database:
  cred = credentials.RefreshToken('./app/config/serviceAccountKey.json')
  default_app = firebase_admin.initialize_app(cred)
