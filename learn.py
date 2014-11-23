import json


def unistring(s):
    return str(s).encode("ascii", "ignore").decode()

# import JSON data as a list of dicts, each of which is a data point
with open("tmp.json") as open_file:
    train = json.loads(unistring(open_file.read()))
for d in train:
    for k in d:
        print(unistring(k), ":", unistring(d[k]))
