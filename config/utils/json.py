import json

def read_json(filename):
    with open("./config/json/" + filename + ".json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open("./config/json/" + filename + ".json", "w") as file:
        json.dump(data, file, indent=4)

def delete_json(filename, object):
    with open("./config/json/" + filename + ".json", "r") as file:
        data = json.load(file)
        data.pop(str(object))
    return data