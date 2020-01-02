import sqlparse,json,os
from DB import *
from functions import *

username = input(">>user: ")
password = input(">>password: ")
user = User(username,password)
print(check_auth(user))

""" check_auth(username,password) """

sqlrequest = get_request();

parsed = sqlparse.parse(sqlrequest)
statement = parsed[0]
""" print(str(statement.tokens[0])+", "+str(statement.tokens[2])) """
if str(statement.tokens[0]) == "create" and str(statement.tokens[2]) == "database": 
    if not exist_db(str(statement.tokens[4])):
        db = Database(user,str(statement.tokens[4]))
        print(db.name)
        db.create_database()
        print("Database "+db.name+" created..")
    else:
        print("La base de donnees "+str(statement.tokens[4])+" existe deja")



if str(statement.tokens[0]) == "use":
    if exist_db(str(statement.tokens[2])):
        f = open(db_files_path+"/"+str(statement.tokens[2])+".json","r+")
        db_tables = json.load(f).get("tables");
        print (db_tables)
        f.close()
        request = get_request()
    else:
        print("la base de donnees n'existe pas")
        
    





