from flask import Flask, jsonify,session
import argparse,json,os,sys
from DB import Database,Champ,User,Table

##Instance de l'application
app = Flask(__name__)
app.secret_key = os.urandom(24)

##PARSE ARGUMENT
def create_parser():
    parser = argparse.ArgumentParser();
    parser.add_argument("create",help="create [--t,--table] or create [--d,--database]")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--t","--table",help="Option pour creer une table");
    group.add_argument("--d","--database",help="Option pour creer une base de donnee");
    return parser.parse_args();

##creer une base de donnee
if create_parser().create == "create" and create_parser().d:
    user = User("cheikh","passer123")
    db = Database(user,create_parser().d)
    db.create_database();
    
##creer une table
if create_parser().create == "create" and create_parser().t:
    table = Table(create_parser().t)
    table.add_attribut(Champ("nom","string","none"))
    table.add_attribut(Champ("prenom","string","none"))
    with open(session.get()+".json", "a") as f:
        f.write(json.load(f).get('tables'))

@app.route('/')
def index():
    session['key'] = 'mou'
    return "session created"

if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=5655)