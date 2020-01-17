import parser
import function
import json


def sgbd():
    lifetime = True
    db = function.convert('./databases/db2.json')
    
    with open('./databases/db1.json','w') as database:
        json.dump(db, database)
        
        
    while(lifetime):
        sql = input(">>")
        state = False
        with open('./databases/db1.json') as database:
            # parser.updateQueryParser(sql, database)
            state = parser.insertQueyParser(sql, database)
            if(state != False):
                (table, columns, values) = state
                res = function.insert('./databases/db1.json',table,columns,values)
                if res:
                    print("Insertion avec success")
                else:
                    print("Erreur d'insertion")