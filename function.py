import json

def insert(db, table, columns, values):
    with open(db) as database:
        database = json.load(database)
        if len(columns) == 0: 
            columns = [i for i in database[table]]
        for col, val in zip(columns, values):
            if "'" not in val:
                try:
                    val = int(str(val))
                except ValueError :
                    print("Erreur de type")
                    print("Le type du champ " + col + " ne correspond pas à la valeur que vous voulez inserer")
                    return False
            elif "'" in val: 
                val = val[1:-1]
            database[table][col] = val
        with open(db, 'w') as json_file:
            json.dump(database, json_file, indent=4)
        return True    