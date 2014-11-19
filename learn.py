import json

# import JSON data as a list of dicts, each of which is a data point
with open("train.json") as open_file:
    file_string = open_file.read().encode("ascii", "ignore").decode()
    train = json.loads(file_string)
print(train)
