from flask import Flask

app = Flask(__name__)
app.secret_key = 'THIS 8mBEvwrng4P!c8nUsyVgJY-jL2mNX6iTIS SUPER SEC!!!8mBEvwrng4P!c8nUsyVgJY-jL2mNX6iTuHmywK!6RHNHkpUfuxCGwW.TYxxo_Yfx'
# NOTE: change secret key if deploying (currently this app runs exclusively as a local client)

from app import routes
