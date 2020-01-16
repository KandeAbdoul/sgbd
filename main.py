from flask import Flask, jsonify,session,request,render_template,redirect,url_for
import argparse,json,os,sys
from functions import *
from passlib.hash import sha256_crypt

##Instance de l'application
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template("index.html");

@app.route('/auth',methods = ['GET','POST'])
def auth():
    if request.method == 'POST':
        user = User(request.form["id"],request.form["password"])
        if check_auth(user):
            return redirect('/')
        else:
            return render_template("auth.html",msg = "Identifiant ou mot de passe incorrecte")
    return render_template("auth.html");

if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=8889)