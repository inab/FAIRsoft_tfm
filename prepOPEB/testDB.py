import json
from pymongo import MongoClient

client = MongoClient()

with open('bioconductor2000.json', 'r') as infile:
    tools = json.load(infile)

db = client.FAIRsoft
testDB = db.test

def replaceDot(d):
    new = {}
    for k in d.keys():
        v = d[k]
        if isinstance(v, dict):
            v = replaceDot(d[k])
        new[k.replace('.', '-')] = v
    return new


for tool in tools:
    tool['integrated']=False
    tool = replaceDot(tool)
    #print(tool)
    testDB.insert_one(tool)
