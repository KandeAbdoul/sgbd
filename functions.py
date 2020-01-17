import os,json,sys,sqlparse
from DB import Champ
##globales path variables
db_files_path = os.getcwd()+"/db_files/"
user_files_path = os.getcwd()+"/user_files/files.json"

def get_request():
    sqlrequest = ""
    while True:
        sqlrequest += input(">>")+" "
        if ';' in sqlrequest:
            break;  
    return sqlrequest

def show_databases(user):
    f = open(user_files_path,"r+")
    users = json.load(f).get('users')
    f.close()
    for u in users:
        if (u["id"] == user.id) and (u["password"] == user.password):
            print("+-----------------------+\n|\t Databases\t|\n+-----------------------+")
            for db in u["databases"]:
                print("|"+db+"\t\t|")
            print("+-----------------------+")

def show_tables(db_name):
    f = open(db_files_path+db_name+".json","r+")
    tables = json.load(f).get('tables')
    f.close()
    print("+-----------------------+\n|\t Tables\t\t|\n+-----------------------+")
    for table in tables:
        print("|"+table["nom"]+"\t\t|")
    print("+-----------------------+")

def exist_table(dbname,tablename):
    f = open(db_files_path+dbname+".json","r+")
    db_tables = json.load(f).get("tables");
    f.close()
    for table in db_tables:
        if tablename == table["nom"]:
            return True
    return False

def is_db_owner(user,db_name):
    f = open(user_files_path,"r+")
    users = json.load(f).get('users')
    f.close()
    for use in users:
        if use["id"] == user.id and use["password"] == user.password and db_name in use["databases"]:
            return True
    return False

def exist_db(db):
    dbs = os.listdir(db_files_path);
    if db+'.json' in dbs:
        return True;
    return False

def exist_user(username):
    with open(user_files_path,"r+") as f:
        users = json.load(f).get('users')
        for user in users:
            if user["id"] == username:
                return True
    return False

def check_auth(user):
    if exist_user(user.id):
        with open(user_files_path,"r+") as f:
            users = json.load(f).get('users')
            for us in users:
                if user.password == us["password"]:
                    return True
            return False
    return False

def create_table(command,user,db_name,table_name):
    if not exist_table(db_name,table_name):
        f = open(db_files_path+db_name+".json","r+")
        db_tables = json.load(f).get("tables");
        f.close()
        db_champs = []
        champs = command.split("(")[1].split(",")
        for champ in champs:
            key = ["none","primary","foreign"]
            key_t = "none"
            if (len(champ.split()) == 3) :
                if champ.split()[2] == ");":
                    pass
                elif champ.split()[2] in key:
                    key_t = champ.split()[2]
                else:
                    print("Erreur synthaxique,revoyer la documentation sur la creation de table")
                    break
            attribut = Champ(champ.split()[0],champ.split()[1],key_t)
            db_champs.append(attribut.create_champ())
        db_tables.append({
            "nom":table_name,
            "champs":db_champs
        })
        with open(db_files_path+"/"+db_name+".json","w") as f:
            f.write(json.dumps({
                "user_id":user.id,
                "nom":db_name,
                "tables":db_tables
            },indent=4))
            f.close()
        print("Table "+table_name+" created...")
    else:
        print("La table "+table_name+" existe deja dans "+db_name)
    
def showcase():
    print("\nWelcome to the SGBD monitor.  Commands end with ;.\n"+
            "Your SGBD connection server is running on port 8888\n "+
            "Server version: 5.7.28-0ubuntu0.18.04.4 (Ubuntu)\n"+
            "Copyright (c) 2019, 2020, Oracle and/or its affiliates. \n"+
            "All rights reserved. Oracle is a registered trademark of Oracle \nCorporation and/or its"+
            "affiliates. Other names may be trademarks of their respective \nowners."+
            "Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.\n\n")

        
##Classe base de donnee
class Database():
    def __init__(self,user,name):
        self.user = user
        self.name = name
        self.tables = []
    
    def add_table(self,table):
        self.tables.append(table)

    def create_database(self):
        ##Creer un fichier json de la base de donnees
        f_db = open(db_files_path+self.name+".json", "w")
        format_db = {
                    "user_id":self.user.id,
                    "nom":self.name,
                    "tables":self.tables 
            }
        f_db.write(json.dumps(format_db,indent=4))
        f_db.close()
        self.user.create_user(self.name)

##Classe utilisatur
class User():
    def __init__(self,id,password):
        self.id = id
        self.password = password
        self.databases = []

    def create_user(self,db_name):
        f_user = open(user_files_path,"r+")
        users = json.load(f_user).get("users")
        f_user.close()
        if not exist_user(self.id):
            ##Creer un fichier json de l'utilisateur de la base de donnees
            new_user = {
                    "id":self.id,
                    "password":self.password,
                    "databases":[]
            }
            users.append(new_user)
        else:
            for user in users:
                if (user["id"] == self.id) and (user["password"] == self.password):
                    user["databases"].append(db_name)
                    break
        format_db = {
                "users":users
            }
        f_user = open(user_files_path,"w")
        f_user.write(json.dumps(format_db,indent=4))
        f_user.close()


##Classe table     
class Table():
    def __init__(self,nom):
        self.nom = nom
        self.champs = []

    def add_attribut(self,champ):
        self.champs.append(champ)
    def create_table(self):
        pass
##Classe champs
class Champ():
    def __init__(self,nom,type,cle):
        self.nom = nom
        self.type = type
        self.cle = cle
    def create_champ(self):
        return {
            "nom":self.nom,
            "type":self.type,
            "cle":self.cle
        }

