# import json

# def convert(file):
#     data = json.load(open(file, 'r'))
#     champ = []
#     file = {}

#     for table in data['tables']:
#     file.update({table['nom']:[]})
#     champ.append(table['champs'][0])
#     i= 0
#     for row in file:
#         file[row].append(champ[i])
#         i=i+1
#     return json.dumps(file, indent=4)