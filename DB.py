import json,os
from functions import *
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
                    "databases":[db_name]
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
##Classe champs
class Champ():
    def __init__(self,nom,type,cle):
        self.nom = nom
        self.type = type
        self.cle = cle

