# Milestone 2

### Video Link
* [put the video link here](https://www.youtube.com)

### Meeting Notes
* Reviewing Firebase + database schemas
* Reviewing current progress on chat app functionality
* Discussion of encryption method and process
* Upcoming steps for chat app + integrating encryption

### Action Items
*

### Contributions
* [Latest Commit](https://github.com/ECS153/final-project-flask-encryption-webapp/commit/d5498811d9fbf7b1d5d99cf9248bdb9fc5c5f1c9)

#### Karmit
* Last Week:
* This Week:
* Blocked:

#### Noah
* Last Week: Finished the database wrapper + authentication. Created the log in and sign up flow and create entries in the database for each user that logs in.
* This Week: Integrating encryption into messages, database/authentication design doc, and create network logging to monitor messages/prove encryption works
* Blocked: None

#### Sam:
* Last Week:
* This Week:
* Blocked:

---

# Milestone 1

### Video Link
* [unlisted Youtube link](https://youtu.be/rFfZddmc-qc)

### Meeting Notes
* Reviewing project file structure
* Reviewing Firebase project requirements
* Overview of inbox-style message flow from client to server to client

### Action Items
* Finalize database schemas, set up [database.py](../web/flaskapp/app/database.py) wrapper for database access and create tables in Firestore
* Set up authentication in Firebase - determine if using email or phone
* Set up login page in HTML using above authentication method
* Initial basic chat features (unencrypted) - frontend HTML UI layout and inbox-style sending messages
* __Design Docs__: database + API wrapper, messaging system and data flow
* Encryption will be a design doc for Milestone 3

### Contributions
* [Latest commit](https://github.com/ECS153/final-project-flask-encryption-webapp/commit/f166101a4c80ae9a5aad59548d0f2d205e64248d)
#### Karmit
* Last Week: Set up Firebase and Flask project structure, enabling service acount permissions.
* This Week: Set up messaging system and data flow, coordinating with Noah's database wrappers.
* Blocked: None
#### Noah
* Last Week: Set up the Firebase API to our Python code and initialized the database connection with the correct permissions.
* This Week: Write database wrapper for Firebase API as well as set up users, messages, and authentication tables accordingly.
* Blocked: None
#### Sam
* Last Week: Catching up with everyone on learning how to use Flask
* This Week: Researching encryption libraries and methods.
* Blocked: None
