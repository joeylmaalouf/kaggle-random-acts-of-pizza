import json


def unistring(s):
    return str(s).encode("ascii", "ignore").decode()

# import JSON data as a list of dicts, each of which is a data point
with open("train.json") as open_file:
    train = json.loads(unistring(open_file.read()))
#print(str(train).encode("ascii", "ignore").decode())
for d in train:
    for i in d:
        print(unistring(i))
