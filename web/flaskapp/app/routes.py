from app import app
from flask import render_template, request, session, redirect, url_for, session
import app.database as db

@app.route("/", methods=['GET', 'POST'])
def index():
  database = db.Database()
  return render_template('index.html', title="Home")

# @LoginRequired  # FIXME: uncomment
@app.route("/inbox", methods=['GET', 'POST'])
def inbox():
  database = db.Database()

  # query all messages for this user
  # query messages table for each message

  conversations = ["asdf1", "asdf2"]  # array of mesage IDs
  messages = {
    "asdf1": {
      "participants": [
        "userID1",
        "userID2"
      ],
      "messages": [
        {
          "timestamp": "this is a timestamp",
          "sender": "userID1",
          "messageContents": "Hi this is our first message"
        },
        {
          "timestamp": "most recent timestamp",
          "sender": "userID2",
          "messageContents": "Hi this is my response to your message"
        }
      ]
    },
    "asdf2": {
      "participants": [
        "userID1",
        "userID3"
      ],
      "messages": [
        {
          "timestamp": "this is a timestamp",
          "sender": "userID1",
          "messageContents": "Hi this is our first message for other conv"
        },
        {
          "timestamp": "this is a timestamp after the first one",
          "sender": "userID3",
          "messageContents": "Hi this is my response to your message"
        },
        {
          "timestamp": "another timestamp that is more recent",
          "sender": "userID3",
          "messageContents": "i sent another message to you"
        }
      ]
    }
  }

  # order the "conversations" array so message IDs are in order of most recent conversations first
  
  return render_template('inbox.html', title="Inbox", conversations=conversations, messages=messages)
