import json,os
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
        f_db = open(os.getcwd()+"/db_files/"+self.name+".json", "w")
        format_db = {
                    "user_id":self.user.id,
                    "nom":self.name,
                    "tables":self.tables 
            }
        f_db.write(json.dumps(format_db,indent=4))
        f_db.close()
        self.create_user()

    def create_user(self):
        ##Creer un fichier json de l'utilisateur de la base de donnees
        f_user = open(os.getcwd()+"/user_files/files.json","r+")
        users = json.load(f_user).get("users")
        new_user = {
                "id":self.user.id,
                "password":self.user.password
        }
        users.append(new_user)
        format_db = {
            "users":users
        }
        f_user.close()
        f_user = open(os.getcwd()+"/user_files/files.json","w")
        f_user.write(json.dumps(format_db,indent=4))
        f_user.close()
##Classe utilisatur
class User():
    def __init__(self,id,password):
        self.id = id
        self.password = password
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

