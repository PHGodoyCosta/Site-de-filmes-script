import json

def get_preload_variables():
    file = open(f"preload.json", "r+").read()
    
    return json.loads(file)

a = get_preload_variables()

print(a["name"])