import sqlparse,json,os,sys
""" from DB import * """
from functions import *
''' from passlib.hash import sha256_crypt
sha256_crypt.verify([secret], [hash]) '''

out = False;
tentative = 0
while True:
    username = input(">>user: ").strip()
    password = input(">>password: ").strip()
    user = User(username,password)
    if check_auth(user):
        print("Authentication success..")
        break
    tentative = tentative + 1
    if tentative == 3:
        print("Authentication failed..")
        sys.exit(0)
##Message d'accueil
showcase()
""" check_auth(username,password) """
while not out:
    sqlrequest = get_request();
    if sqlrequest == "exit;":
        print("dougouna fi")
        out = True
        break
    sqlrequest = sqlrequest.split(";")[0].split()
    ##Creer un utilisateur
    if len(sqlrequest) == 6 and sqlrequest[0] == 'create' and sqlrequest[1]=='user' and sqlrequest[3] == 'identified' and sqlrequest[4]=='by':
        u = User(sqlrequest[2],sqlrequest[5])
        if not check_auth(u):
            user.create_user("")
            print("user created...")
        else:
            print("L'utilisateur existe déja")
    ##Afficher les bases de donnees de l'utilisateur connecte
    elif len(sqlrequest) == 2 and sqlrequest[0] == 'show' and sqlrequest[1]=='databases':
        show_databases(user)
    ##Creer une base de donnee
    elif len(sqlrequest) == 3 and sqlrequest[0] == 'create' and sqlrequest[1]=='database' and sqlrequest[2] != '':
        if not exist_db(sqlrequest[2]):
            db = Database(user,sqlrequest[2])
            db.create_database()
            print("Database "+db.name+" created..")
        else:
            print("La base de donnees "+sqlrequest[2]+" existe deja")
    ##Acceder a une base de donnees
    elif len(sqlrequest) == 2 and sqlrequest[0] == "use" and sqlrequest[1] != '':
        if exist_db(sqlrequest[1]) and is_db_owner(user,sqlrequest[1]):
            print("using database "+sqlrequest[1]+"...")
            while True:
                request = get_request()
                print(request.split()[1].split(";"))
                sub_request = request.split("(")[0].split();
                ##Creer une table
                if len(sub_request) == 3 and sub_request[0] == "create" and sub_request[1]=="table" and sub_request[2] != '':
                    create_table(request,user,sqlrequest[1],sub_request[2]);
                elif len(request.split()) == 2 and request.split()[0] == 'show' and request.split()[1].split(";")[0]=='tables':
                    ##Afficher les bases de donnees de l'utilisateur connecte
                    show_tables(sqlrequest[1])
                else:
                    print("Erreur synthaxique,revoyer la documentation sur la creation de table")
                
                request = ""
        else:
            print("la base de donnees n'existe pas ou vous n'en etes pas propriétaire")   
    else:
        print("Erreur synthaxique,revoyer la documentation de ce systeme de gestion de bases de donnees")
    sqlrequest = ""





