import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys


def unistring(s):
    return str(s).encode("ascii", "ignore").decode()


def relevant_data_string(d):
    return pad_num_str(d["requester_account_age_in_days_at_request"], 12, 6) \
        + "     " \
        + pad_num_str(d["requester_upvotes_minus_downvotes_at_request"], 6, 0) \
        + "       " \
        + str(d["requester_received_pizza"])


def pad_num_str(s, N, n):
    return ("%0"+str(N)+"."+str(n)+"f") % float(s)


def will_reciprocate(d):
    title = d["request_title"].lower()
    text = d["request_text_edit_aware"].lower()
    phrases = ["pay it forward", "return the favor", "reciprocate"]
    for p in phrases:
        if p in title or p in text:
            return True
    return False


def get_data(data_object, key1x, key2y, key3z):
    dataX = []
    dataY = []
    dataZ = []
    for d in data_object:
        dataX.append(float(d[key1x]))
        dataY.append(float(d[key2y]))
        dataZ.append(str(d[key3z]) == "True")
    return {"x": dataX, "y": dataY, "z": dataZ}


def scatterplot(data):
    for i in range(len(data["x"])):
        formatting = "." + ("g" if data["z"][i] else "r")
        plt.plot(data["x"][i], data["y"][i], formatting)
    coeffs = np.polyfit(x=data["x"], y=data["y"], deg=1)
    poly = np.poly1d(coeffs)
    plt.plot(data["x"], poly(data["x"]))
    plt.show()


def main(argv):
    # import JSON data as a list of dicts, each of which is a data point
    with open("train.json") as open_file:
        train = json.loads(unistring(open_file.read()))
#   print("account age      up - down    recieved pizza?")
#   for d in train:
#       print(relevant_data_string(d))
#       for k in d:
#           print(unistring(k), ":", unistring(d[k]), "\n")
    data_dict = get_data(train, "requester_account_age_in_days_at_request",
                         "requester_upvotes_minus_downvotes_at_request",
                         "requester_received_pizza")
    scatterplot(data_dict)

if __name__ == "__main__":
    main(sys.argv)
