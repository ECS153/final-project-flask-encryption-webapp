# Milestone 3

### Video Link
* [Milestone 2 video](http://www.youtube.com)

### Meeting Notes
* Decided that a logger was not necessary as well placed print statements/looking in the web client would be enough to prove encryption, especially because presentation is pre-recorded
* Discussion with Sam regarding encryption function wrappers
* Discussing the current issue of being unable to read your own messages after encrypting them for the recipient.

### Action Items
* Check if private key exists locally on login. If not, prompt user to import their private key file
* Finalize encryption integration into chat
* Fix issue of encrypting own chats with other user's public key (unable to read own chats)

### Contributions
* [Latest Commit](https://github.com/ECS153/final-project-flask-encryption-webapp/commit/eb3af0e34abf2eb0f25c19182b05f733c98783c6)

#### Karmit
* Last Week: Integrating encryption function wrappers into chat code, design doc for messaging and data flow, local storage and sending public key to database.
* This Week: Finish encrypting chats, importing private key into new devices.
* Blocked: None

#### Noah
* Last Week: Implimented local storage for the private key. Design doc for database and authentication.
* This Week:
* Blocked: None

#### Sam:
* Last Week:
* This Week:
* Blocked: none

---

# Milestone 2

### Video Link
* [Milestone 2 video](https://youtu.be/2h5dWP1_BaE)

### Meeting Notes
* Reviewing Firebase + database schemas
* Reviewing current progress on chat app functionality
* Discussion of encryption method and process
* Upcoming steps for chat app + integrating encryption

### Action Items
* Function wrappers for generating account key pairs
* Incorporate local storage for private keys, database storage for public keys. Potentially considering a solution of having a long seed for the user to re-generate key pairs on a new device.
* Encrypting messages before sending to database. Decrypting after receiving
* Design docs for database/authentication and messaging/data flow

### Contributions
* [Latest Commit](https://github.com/ECS153/final-project-flask-encryption-webapp/commit/d5498811d9fbf7b1d5d99cf9248bdb9fc5c5f1c9)

#### Karmit
* Last Week: Chat app functionality (unencrypted), integrating with database, local storage, initial chat UI.
* This Week: Integrating encryption into chat, local storage, design doc for messaging system and data flow.
* Blocked: None

#### Noah
* Last Week: Finished the database wrapper + authentication. Created the log in and sign up flow and create entries in the database for each user that logs in.
* This Week: Integrating encryption into messages, database/authentication design doc, local storage, and create network logging to monitor messages/prove encryption works
* Blocked: None

#### Sam:
* Last Week: Researching libraries and deciding cryptography system to use along with where to store keys.
* This Week: Working on wrapper function for generating keys to be used by the other developer.
* Blocked: none

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
