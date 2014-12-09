import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys


def get_data(data_object, key1x, key2y, key3z):
    dataX = []
    dataY = []
    dataZ = []
    for d in data_object:
        dataX.append(float(d[key1x]))
        dataY.append(float(d[key2y]))
        dataZ.append(str(d[key3z]) == "True")
    return {"x": dataX, "y": dataY, "z": dataZ}


def scatterplot(data_dict):
    for i in range(len(data_dict["x"])):
        formatting = "." + ("g" if data_dict["z"][i] else "r")
        plt.plot(data_dict["x"][i], data_dict["y"][i], formatting)
    coeffs = np.polyfit(x=data_dict["x"], y=data_dict["y"], deg=1)
    poly = np.poly1d(coeffs)
    plt.plot(data_dict["x"], poly(data_dict["x"]))
    plt.show()


def print_data(data_dict):
    print("account age      up - down    recieved pizza?")
    for i in range(len(data_dict["x"])):
        print(
            pad_num_str(data_dict["x"][i], 12, 6)
            + "     "
            + pad_num_str(data_dict["y"][i], 6, 0)
            + "       "
            + str(data_dict["z"][i])
        )


def unistring(s):
    return str(s).encode("ascii", "ignore").decode()


def relevant_data_string(d):
    return pad_num_str(d["x"], 12, 6) \
        + "     " \
        + pad_num_str(d["y"], 6, 0) \
        + "       " \
        + str(d["z"])


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


def main(argv):
    # import JSON data as a list of dicts, each of which is a data point
    with open("train.json") as open_file:
        train = json.loads(unistring(open_file.read()))
    data_dict = get_data(train, "requester_account_age_in_days_at_request",
                         "requester_upvotes_minus_downvotes_at_request",
                         "requester_received_pizza")
    print_data(data_dict)
    scatterplot(data_dict)

if __name__ == "__main__":
    main(sys.argv)
