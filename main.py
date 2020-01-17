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

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html");

@app.route('/tables',methods = ['GET','POST'])
def tables():
    tables = []
    if request.method == 'POST':
        search = request.form['search']
        if exist_db(search) and is_db_owner(User(session['id'],session['pwd']),search):
            print(User(session['id'],session['pwd']))
            f = open(db_files_path+search+".json","r+")
            tables = json.load(f).get('tables');
            f.close()
        else:
            print("Choisissez une base de donnees existantes")
    return render_template("tables.html",tables = tables);

@app.route('/databases')
def databases():
    if 'db' in session:
        print(session['db'])
    return render_template("databases.html",databases = session['db']);

@app.route('/auth',methods = ['GET','POST'])
def auth():
    if request.method == 'POST':
        session['id'] = request.form["id"]
        session['pwd'] = request.form["password"]
        user = User(request.form["id"],request.form["password"])
        if check_auth(user):
            f = open(user_files_path,"r+")
            users = json.load(f).get('users');
            f.close()
            dbs = [use["databases"] for use in users if ((user.id == use["id"]) and (user.password == use["password"])) ]
            session['db'] = dbs[0]
            return redirect('/')
        else:
            return render_template("auth.html",msg = "Identifiant ou mot de passe incorrecte")
    return render_template("auth.html");

if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=8889)