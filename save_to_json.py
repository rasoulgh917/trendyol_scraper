import json
from logger_ import logger
from os import path

def to_json(p_dict, filename, cnt):
    if path.exists(filename) == True:
        f = open(filename, "r")
    else:
        f = open(filename, "x")
        f.close()
        f = open(filename, "r")
    try:
        dict_ = json.loads(f.read())
        dict_['results'].append(p_dict)
        dict_['results_count'] += 1
    except:
        dict_ = {}
        dict_['results_count'] = 1
        dict_['results'] = []
        dict_['results'].append(p_dict)
    f.close()
    f = open(filename, 'w')
    f.write(json.dumps(dict_, indent=4))
    f.close()
