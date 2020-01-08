from flask import Flask, jsonify,session
import argparse,json,os,sys
from DB import Database,Champ,User,Table

##Instance de l'application
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return 

if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=5655)