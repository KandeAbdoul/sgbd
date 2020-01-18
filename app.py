import sqlparse,json,os,sys
""" from DB import * """
from parser import *
from functions import *
import socket
from  threading import  Thread
''' from passlib.hash import sha256_crypt
sha256_crypt.verify([secret], [hash]) '''
''' from flask import  Flask

app = Flask(__name__)
@app.route('/')
def main():
    return sgbd() '''

def sgbd(socket_instance):
    connect = True;
    tentative = 0
    connection, address = socket_instance.accept()
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
    while connect:
        sqlrequest = get_request();
        print(sqlrequest[:5])
        if sqlrequest[:5] == 'exit;':
            sys.exit(0)
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
                db = convert(db_files_path+sqlrequest[1]+".json")
                with open(db_files_path+'db1.json','w') as database:
                    json.dump(db, database,indent=4)
                while True:
                    request = get_request()
                    if request[:5] == 'exit;':
                        sys.exit(0)
                    print(request.split()[1].split(";"))
                    sub_request = request.split("(")[0].split();
                    ##Creer une table
                    if len(sub_request) == 3 and sub_request[0] == "create" and sub_request[1]=="table" and sub_request[2] != '':
                        create_table(request,user,sqlrequest[1],sub_request[2]);
                    elif len(request.split()) == 2 and request.split()[0] == 'show' and request.split()[1].split(";")[0]=='tables':
                        ##Afficher les bases de donnees de l'utilisateur connecte
                        show_tables(sqlrequest[1])
                    elif sub_request[0] == "insert":
                    #####################################################################################
                        state = False
                        with open(db_files_path+'db1.json') as database:
                            # parser.updateQueryParser(sql, database)
                            state = insertQueyParser(request, database)
                            if(state != False):
                                (table, columns, values) = state
                                res = insert(db_files_path+'db1.json',table,columns,values)
                                if res:
                                    print("Insertion avec success")
                                else:
                                    print("Erreur d'insertion")
                    elif sub_request[0] == "select":
                        print(selectQueryParser(request))


                    ######################################################################################
                    else:
                        print("Erreur synthaxique,revoyer la documentation sur la creation de table")
                    
                    request = ""
            else:
                print("la base de donnees n'existe pas ou vous n'en etes pas propriétaire")   
        else:
            print("Erreur synthaxique,revoyer la documentation de ce systeme de gestion de bases de donnees")
        sqlrequest = ""

def socket_provider(host , port):
    
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_instance.bind((host, port))

    socket_instance.listen()

    return socket_instance


#CREATING THREADS

def thread_provider(socket_instance , number_of_connection_to_create):

    for i in range(0,number_of_connection_to_create):

        Thread(target = sgbd , args = (socket_instance,)).start()

given_socket = socket_provider('127.0.0.1' , 8888)

thread_provider(given_socket , 5)
while True:
    given_socket.listen()
    print( "En écoute...")
    (clientsocket, (ip, port)) = given_socket.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()

