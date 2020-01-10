import sqlparse,json,os,sys
""" from DB import * """
from functions import *

exit = False;
tentative = 0
while True:
    username = input(">>user: ")
    password = input(">>password: ")
    user = User(username,password)
    if check_auth(user):
        print("Authentication success..")
        break
    tentative = tentative + 1
    if tentative == 3:
        print("Authentication failed..")
        exit = True
        break

""" check_auth(username,password) """
while not exit:
    ##Message d'accueil
    showcase()
    sqlrequest = get_request();
    if sqlrequest in ["exit;","exit ;"]:
        exit = True
        break
    sqlrequest = sqlrequest.split(";")[0].split()

    if len(sqlrequest) == 3 and sqlrequest[0] == 'create' and sqlrequest[1]=='database' and sqlrequest[2] != '':
        if not exist_db(sqlrequest[2]):
            db = Database(user,sqlrequest[2])
            db.create_database()
            print("Database "+db.name+" created..")
        else:
            print("La base de donnees "+sqlrequest[2]+" existe deja")

    if len(sqlrequest) == 2 and sqlrequest[0] == "use" and sqlrequest[1] != '':
        if exist_db(sqlrequest[1]):
            request = get_request()
            sub_request = request.split("(")[0].split();
            if len(sub_request) == 3 and sub_request[0] == "create" and sub_request[1]=="table" and sub_request[2] != '':
               ##Fonction qui cree une table
               create_table(request,user,sqlrequest[1],sub_request[2]);
               print("Table created...")
            else:
                print("Erreur synthaxique,revoyer la documentation sur la creation de table")
        else:
            print("la base de donnees n'existe pas")
        
    sqlrequest = ""





