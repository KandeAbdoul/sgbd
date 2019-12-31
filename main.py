import parser
import function

lifetime = True
db = './databases/db1.json'
while(lifetime):
    sql = input(">>")
    state = False
    with open(db) as database:
        state = parser.insertQueyParser(sql, database)
    if(state != False):
        (table, columns, values) = state
        res = function.insert(db,table,columns,values)
        if res:
            print("Insertion avec success")
        else:
            print("Erreur d'insertion")
            
    