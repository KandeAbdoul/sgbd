import sqlparse
import re
import json

def getCompSign(cond):
    signComp = ['>=','<=','>','<','<>' ,'=']
    for s in signComp:
        if s in cond:
            return s
        
#Parsing de la condition
def parseCondition(condition):
    cond = ''
    if '(' in condition:
        cond = str(condition[1:-1])
    else:
        cond = condition
    comparator = getCompSign(cond)
    valueComp = cond.split(comparator)
    #espace eeeee
    return valueComp, comparator


def checkCondition(table, cond, comparator):
    values = []
    val = cond[1]
    col = cond[0]
    val = val.split(';')[0]
    if col in table[0]:
        if "'" not in val:
            if(isinstance(table[0][col],int)):
                try:
                    val = int(val)
                except ValueError :
                    print("Erreur de type de ", col)
                    return False
            else: 
                print("Cette colonne ne peut inserer une valeur de ce type")
                return False
        else: 
            val = val[1:-1]
        if(comparator == '>'):
            for row in table:
                for line in row:
                    #print(line)
                    if line == col:
                        if row[line] > val:
                            values.append(row)
        elif(comparator == '<'):
            for row in table:
                for line in row:
                    if line == col:
                        if row[line] < val:
                            values.append(row)
        elif(comparator == '>='):
            for row in table:
                for line in row:
                    if line == col:
                        if row[line] >= val:
                            values.append(row)
        elif(comparator == '<='):
            for row in table:
                for line in row:
                    if line == col:
                        if row[line] <= val:
                            values.append(row)
        elif(comparator == '='):
            for row in table:
                for line in row:
                    if line == col:
                        if row[col] == val:
                            values.append(row)
    else: print("Cette colonne n'existe pas dans la table")
    return values

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
        for t in data[table]:
            if str(i) not in t:
                print("Il n'y pas de colonne nommée ", i)
                notFindColumn = True
                break
    if(notFindColumn): return False
    if len(columns) == len(values):
        return table, columns, values
    elif len(columns) == 0:
        if len(values) == len(data[table][0]):
            return table, columns, values
        else: 
            print("Le nombre de valeurs ne correspondent au nombre de champs de votre table")
            return False
    else: 
        print("Le nombre de valeurs ne correspondent au nombre de champs de votre table")
        return False

def updateQueryParser(sql, database):
    data = json.load(database)
    try:
        parsed = sqlparse.parse(sql)
        stmt = parsed[0]
    except sqlparse.exceptions.SQLParseError:
        print("Erreur sur votre requete sql\n'%s'" % stmt)
        return False
    
    table = stmt.tokens[2]
    query = str(stmt)
    # print(query)
    columnsPart = query[query.index('set') + len("set"):query.index('where')]
    columnsPart = columnsPart.split(",")
    columnsForUpdate = [i.replace(' ','') for i in columnsPart]
    print(columnsForUpdate)
    ConditionColumnsPart = query[query.index('where') + len("where"):]
    print(ConditionColumnsPart)
    
    # columsForUpdate = [i.split(',')[0] for i in columnsPart]
    # print(columsForUpdate)
    # conditionPart = query[query.index('where') + 1:]
    # print(conditionPart)
def selectQueryParser(sql):
    columnsPart = sql[sql.index("select") + len("select") +1:sql.index("from") -1]
    table = sql.split('from',1)[1].split()[0]
    columns = []
    columnsPart = columnsPart.split()
    columnsPart = ''.join(columnsPart)
    with open('./db_files/db1.json') as database:
        #s'il y a un where dans la condition dans la condition
        db = json.load(database)
        if table not in db:
            print("cette table n'existe pas dans votre base de donnees")
            return False
        if 'where' in sql:
            if 'groupe by' not in sql:
                condition = sql[sql.index("where") + len("where") +1:]
                value, comparator = parseCondition(condition)
                if(columnsPart == '*'):
                    return checkCondition(db[table], value, comparator)
                    # for col in db[table]:
                    #     print(col, ': ', db[table][col])
                else:
                    champs = columnsPart.split(",")
                    for i in champs:
                        if ' ' in i:
                            columns.append(i.split()[0])
                        else: columns.append(i)
                    notFindColumn = False
                    for i in columns:
                        for t in db[table]:
                            if str(i) not in t:
                                print("Il n'y pas de colonne nommée ", i)
                                notFindColumn = True
                                break
                    if(notFindColumn): return False
                    tmpresult = checkCondition(db[table], value, comparator)
                    result = []
                    for re in tmpresult:
                        for row in re:
                            for col in columns:
                                if col == row:
                                    result.append({col:re[col]})
                    return result
                    # for col in db[table]:
                    #     for val in columns:
                    #         if(printcol == val):
                    #            print printprint(col, ': ', db[table][col])
        else:
            if(columnsPart == '*'):
                # for row in db[table]:
                #     print(col, ': ', db[table][col])
                return db[table]
            else:
                values = []
                champs = columnsPart.split(",")
                for i in champs:
                    if ' ' in i:
                        columns.append(i.split()[0])
                    else: columns.append(i)
                
                tmp = []
                tmp2 = {}
                for row in db[table]:
                    for col in row:
                        for val in columns:
                            if(col == val):
                                tmp2.update({col:row[col]})
                    tmp.append(tmp2)
                    tmp2 = {}  
                return tmp