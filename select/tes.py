import json
#recuperation du signe de la comparaison
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
    if col in table[0]:
        if "'" not in val:
            if(isinstance(table[0][col],int)):
                try:
                    val = int(str(val))
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

  
#main  

def selecParser(sql):
    columnsPart = sql[sql.index("select") + len("select") +1:sql.index("from") -1]
    table = sql.split('from',1)[1].split()[0] 
    columns = []
    columnsPart = columnsPart.split()
    columnsPart = ''.join(columnsPart)

    with open('../databases/db1.json') as database:
        #s'il y a un where dans la condition dans la condition
        db = json.load(database)
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
                    #         if(col == val):
                    #             print(col, ': ', db[table][col])
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
while 1:
    print(selecParser(input('>>')))