import json


typesMap = {'Command-line tool':'cmd',
    'Web application':'web',
    'Library':'lib',
    'Desktop application':'app',
    'Database portal':'db',
    'Web service':'soap',
    'Web API':'rest',
    'Suite':'suite',
    'Script':'script',
    'Workbench':'workbench',
    'Plug-in':'plugin',
    'Workflow':'workflow',
    'SPARQL endpoint':'sparql',
    'None': 'None'
    }


rawScores = open('scores/FAIRinsts.txt', 'r')
Scores ={}

for line in rawScores:
    line = line.strip()
    fields = line.split('\t')
    Scores[fields[0]] = [float(fields[1]), float(fields[2]), float(fields[3]), float(fields[4])]



with open('metrics.json', 'r') as infile:
    rawMetrics = json.load(infile)
'''
from pymongo import MongoClient
client = MongoClient()
db = client.FAIRmetrics
collection = db.metrics
'''
Metrics = []
for tool in rawMetrics:
    #print(tool['name'])
    #print(tool['version'])
    #print(tool['type'])

    if tool['version']:
        version = tool['version']
    else:
        version = 'None'
    if tool['type']:
        type_ = tool['type']
    else:
        type_ = 'None'

    ID = tool['name'] + '/' + version + '/' + type_
    id_ = tool['name'] + '/' + version + '/' + typesMap[type_]

    metrics = { 'id' : id_ ,
    'F' : {'1. Identity uniqueness':{'1.1. Uniqueness of name': tool['F1_1'],'1.2. Identifiability of version': tool['F1_2'] },
            '2. Existence of Metadata': {'2.1. Structured Metadata': tool['F2_1'], '2.2. Standarized Metadata': tool['F2_2']},
            '3. Searchability': {'3.1. Searchability in registries': tool['F3_1'] ,'3.2. Searchability in software repositories': tool['F3_2'], '3.3. Searchability in literature': tool['F3_3'] }  },
    'A': {'1. Existance of downloadable, buildable or accesible working version':{'1.1. Existence of API or web': tool['A1_1'], '1.2. Existence of downloadable and buildable software working version':tool['A1_2'] ,'1.3. Existence of installation instructions':tool['A1_3'], '1.4. Existence of test data':tool['A1_4'], '1.5. Existence of software source code':tool['A1_5'] },
          '2. Software history trackability': {'2.1. Metadata of previous versions at software repositories':tool['A2_1'], '2.2. Existence of accesible previous versions of the software':tool['A2_2']},
          '3. Restricted access': {'3.1. Registration compulsory':tool['A3_1'], '3.2. Availability of version for free software':tool['A3_2'], '3.3. Availability for several OS':tool['A3_3'], '3.4. Availability on free e-infrastructure':tool['A3_4'], '3.5. Availability on several e-infrastructures':tool['A3_5']} },
    'I': {
        '1. Documentation on input/output datatypes and formats': {'1.1. Usage of standard data formats':tool['I1_1'], '1.2. Usage of standard API framework':tool['I1_2'], '1.3. Verificability of data formats':tool['I1_3'], '1.4. Flexibility of data format supported':tool['I1_4'], '1.5. Generation of provenance information':tool['I1_5'] },
        '2. Workflow compatibility': {'2.1. Existence of of API/library version':tool['I2_1'], '2.2. E-infrastructure compatibility':tool['I2_2']},
        '3. Dependencies availability': {'3.1. Dependencies statement':tool['I3_1'], '3.2. Dependencies are provided':tool['I3_2'], '3.3. Availability through dependencies aware systems':tool['I3_3']}},
    'R': {'1. Existence of usage documentation' : {'1.1. Existence of usage guides':tool['R1_1'], '1.2. Existence of conditions of use':tool['R1_2']},
        '2. Existence of License': {'2.1. Existence of terms of use':tool['R2_1'], '2.2. Existence of conditions of use':tool['R2_2']},
        '3. Existence of contribution policy': {'3.1. Contributors policy specification':tool['R3_1'], '3.2. Existence of credit': tool['R3_2']},
        '4. Provenance availability': {'4.1. Usage of version control':tool['R4_1'], '4.2. Existence of release policy': tool['R4_2'], '4.3. Metadata of previous versions at software repositories':tool['R4_3']}},
    'scores': Scores[ID],
    'type': typesMap[type_],
    'version': version,
    'name': tool['name']
    }
    Metrics.append(metrics)
    #collection.insert_one(metrics)

'''
'F' : {'1':{'1': tool['F1_1'],'2': tool['F1_2'] },
        '2': {'1': tool['F2_1'], '2': tool['F2_2']},
        '3': {'1': tool['F3_1'] ,'2': tool['F3_2'], '3': tool['F3_3'] }  },
'A': {'1':{'1': tool['A1_1'], '2':tool['A1_2'] ,'3':tool['A1_3'], '4':tool['A1_4'], '5':tool['A1_5'] },
      '2': {'1':tool['A2_1'], '2':tool['A2_2']},
      '3': {'1':tool['A3_1'], '2':tool['A3_2'], '3':tool['A3_3'], '4':tool['A3_4'], '5':tool['A3_5']} },
'I': {
    '1': {'1':tool['I1_1'], '2':tool['I1_2'], '3':tool['I1_3'], '4':tool['I1_4'], '5':tool['I1_5'] },
    '2': {'1':tool['I2_1'], '2':tool['I2_2']},
    '3': {'1':tool['I3_1'], '2':tool['I3_2'], '3':tool['I3_3']}},
'R': {'1' : {'1':tool['R1_1'], '2':tool['R1_2']},
    '2': {'1':tool['R2_1'], '2':tool['R2_2']},
    '3': {'1':tool['R3_1'], '2': tool['R3_2']},
    '4': {'1':tool['R4_1'], '2': tool['R4_2'], '3':tool['R4_3']}},
'scores': Scores[ID],
'''


with open('metrics_OPEB.json', 'w') as outfile:
    json.dump(Metrics, outfile)
