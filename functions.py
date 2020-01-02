import os,json
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
        