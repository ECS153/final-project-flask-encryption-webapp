import firebase_admin
import datetime
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

  def createMessage(self, to, sender, messageText):
    """ Creates a message from to to sender containing the message """
    db = firestore.client()
    message = {
      'participants': [to, sender],
      'messages': [
        {
          "timestamp": datetime.datetime.now(),
          "sender": sender,
          "messageContents": messageText
        }
      ]
    }

    (_, message) = db.collection('messages').add(message)

    messageId = message.id

    db = firestore.client()
    user = db.collection('users').document(to)

    if user.get().to_dict() is None:
      # the userID for to does not exist
      return
    user.update({
      'messages': firestore.ArrayUnion([messageId])
    })

    db = firestore.client()
    user = db.collection('users').document(sender)
    user.update({
      'messages': firestore.ArrayUnion([messageId])
    })

    return

  def replyToMessage(self, messageId, sender, messageText):
    db = firestore.client()
    message = db.collection('messages').document(messageId)

    reply = {
      "timestamp": datetime.datetime.now(),
      "sender": sender,
      "messageContents": messageText
    }

    message.update({
      'messages': firestore.ArrayUnion([reply])
    })

    return

  def getInbox(self, userId):
    db = firestore.client()
    user = db.collection('users').document(userId)
    messages = user.get().to_dict()['messages']

    allMessages = {}

    for messageId in messages:
      db = firestore.client()
      message = db.collection('messages').document(messageId)
      allMessages[messageId] = message.get().to_dict()

    return allMessages


