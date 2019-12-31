import sqlparse
import re
import json
import function


def getValue(params):
    values = []
    for word in params.split('(')[1].split(','):
        word = word.split(' ')
        val = ''
        if len(word) == 1: val = word[0]
        elif len(word) == 2: val = word[1]
        if ')' in val: val=val[:-1]
        values.append(val)
    return values

def insertQueyParser(sql, database):
    data = json.load(database)
    try:
        parsed = sqlparse.parse(sql)
        stmt = parsed[0]
    except sqlparse.exceptions.SQLParseError:
        print("Erreur sur votre requete sql\n'%s'" % stmt)
        return False
        
    table = ''
    tablepart = str(stmt.tokens[4])
    columns = []
    if '(' in tablepart: 
        table = tablepart.split('(')[0]
        columnsPart = str(stmt.tokens[4])
        columns = getValue(columnsPart)
    else: table = tablepart
    if table not in data:
        print("cette table n'existe pas dans votre base de donnees")
        return False
    valuesPart = str(stmt.tokens[6])
    values = getValue(valuesPart)
    notFindColumn = False
    for i in columns:
        if str(i) not in data[table]:
            print("Il n'y pas de colonne nommée ", i)
            notFindColumn = True
            break
    if(notFindColumn): return False
    if len(columns) == len(values):
        return table, columns, values
    elif len(columns) == 0:
        if len(values) == len(data[table]):
            return table, columns, values
        else: 
            print("Le nombre de valeurs ne correspondent au nombre de champs de votre table")
            return False
    else: 
        print("Le nombre de valeurs ne correspondent au nombre de champs de votre table")
        return False
