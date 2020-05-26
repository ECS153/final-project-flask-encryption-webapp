import firebase_admin
import datetime
import app.encryption as encrypt
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore


class Database:
  cred = credentials.Certificate('./app/config/serviceAccountKey.json')
  default_app = firebase_admin.initialize_app(cred)

  def CreateUser(self, user):
    """ Creates a new user in the 'users' table in firestore. User is a firebase admin user object. Returns the new users public key """
    db = firestore.client()
    doc_ref = db.collection('users').document(user.email)
    public, private = encrypt.GenerateKeyPair(seed=None)

    data = {}
    path = './app/config/privateKey.json'
    import json

    try:
      with open(path, "r+") as f:
        data = json.load(f)
    except:
      print("File does not exist.")

    with open(path, "w+") as f:
      data[user.email] = private
      f.truncate(0)
      json.dump(data, f)

    doc_ref.set({
      'userId': user.uid,
      'name': user.display_name,
      'email': user.email,
      'publicKey': public,
      'messages': []
    })

    return (public, private)

  def CreateMessage(self, to, sender, messageText):
    """ Creates a message from to to sender containing the message """
    db = firestore.client()
    user = db.collection('users').document(to)

    if user.get().to_dict() is None:
      return "That user does not exists"


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
    user.update({
      'messages': firestore.ArrayUnion([messageId])
    })

    db = firestore.client()
    user = db.collection('users').document(sender)
    user.update({
      'messages': firestore.ArrayUnion([messageId])
    })

    return ""

  def ReplyToMessage(self, messageId, sender, messageText):
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

  def GetInbox(self, userId, privateKey):
    db = firestore.client()
    user = db.collection('users').document(userId)
    messages = user.get().to_dict()['messages']

    allMessages = {}
    conversations = []

    for messageId in messages:
      db = firestore.client()
      message = db.collection('messages').document(messageId)
      allMessages[messageId] = message.get().to_dict()
      conversations.append((allMessages[messageId]['messages'][-1]['timestamp'].timestamp(), messageId)) # Gets the most recent messages timestamp


    def GetKey(item):
      return item[0]

    conversations = sorted(conversations, key=GetKey, reverse=True)

    for msgId, msgObj in allMessages.items():
      for messageArray in msgObj["messages"]:
        messageArray["messageContents"] = encrypt.Decrypt(privateKey, messageArray["messageContents"])

    return allMessages, conversations

  def GetPublicKeyForUser(self, email):
    try:
      db = firestore.client()
      key = db.collection('users').document(email)
      publicKey = key.get().to_dict()['publicKey']
      return publicKey
    except:
      return False
