import json

def insert(db, table, columns, values):
    with open(db) as database:
        database = json.load(database)
        if len(columns) == 0: 
            for row in database[table]:
                for line in row:
                    columns.append(line)
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
            i = 0
            for row in database[table]:
                for line in row:
                    if line == col:
                        database[table][i][line] = val
                i=i+1
        with open(db, 'w') as json_file:
            json.dump(database, json_file, indent=4)
        return True    
    
def convert(f):
    data = json.load(open(f, 'r'))
    champ = []
    files = {}

    for table in data['tables']:
        files.update({table['nom']:[]})
        champ.append(table['champs'][0])
    i= 0
    for row in files:
        files[row].append(champ[i])
        i=i+1
    return files