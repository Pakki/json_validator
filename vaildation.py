import os
import json
import jsonschema
from jsonschema import validate


EVENTDIR = 'task_folder/event'
SCHEMADIR = 'task_folder/schema'


def loadJson(filename):
    
    try:
        with open(filename, 'r') as readFile:
            jsonObject = json.load(readFile)
    except ValueError as err:
        return err
    return jsonObject


def validateJson(jsonObject, filename):
    try:
        validate(instance=jsonObject, schema=schemes[jsonObject['event']])

    except jsonschema.exceptions.ValidationError as err:
        print(f'file {filename} is not valid - {err.message}')
        return

    print(f'file {filename} is valid JSON file')




schemes = {}
#make a collection of schemas
for filename in os.listdir(path=SCHEMADIR):
    jsonObject = loadJson(SCHEMADIR + '/' + filename)
    if jsonObject is None:
        print(f"file {filename} is not a valid JSON file")
        continue
    else:
        schemes[filename.split('.')[0]] = jsonObject


for filename in os.listdir(path=EVENTDIR):
    jsonObject = loadJson(EVENTDIR + '/' + filename)

    #first - check json file
    if jsonObject is None:
        print(f"file {filename} is broken JSON file")
        continue
    if 'event' in jsonObject.keys():
        
        #if json file is ok - try to validate it by schema
        if jsonObject['event'] in schemes.keys():
            validateJson(jsonObject, filename)
            
        else:
            print(f"file {filename} is not validated - there are no scheme '{jsonObject['event']}' in schemes")
    else:
        print(f"file {filename} has no 'event' attribute")

    

    


