import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys


def get_data(data_object, key1, renamed1, key2, renamed2, key3, renamed3):
    val1 = []
    val2 = []
    val3 = []
    for d in data_object:
        val1.append(float(d[key1]))
        val2.append(float(d[key2]))
        val3.append(str(d[key3]) == "True")
    return {renamed1: val1, renamed2: val2, renamed3: val3}


def scatterplot(data_dict):
    for i in range(len(data_dict["age"])):
        formatting = "." + ("g" if data_dict["result"][i] else "r")
        plt.plot(data_dict["age"][i], data_dict["karma"][i], formatting)
    coeffs = np.polyfit(x=data_dict["age"], y=data_dict["karma"], deg=1)
    poly = np.poly1d(coeffs)
    plt.plot(data_dict["age"], poly(data_dict["age"]))
    plt.show()


def print_data(data_dict):
    print("age, karma, result")
    for i in range(len(data_dict["age"])):
        print(
            pad_num_str(data_dict["age"][i], 12, 6),
            pad_num_str(data_dict["karma"][i], 6, 0),
            str(data_dict["result"][i])
        )


def unistring(s):
    return str(s).encode("ascii", "ignore").decode()


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
    data_dict = get_data(train,
                         "requester_account_age_in_days_at_request",
                         "age",
                         "requester_upvotes_minus_downvotes_at_request",
                         "karma",
                         "requester_received_pizza",
                         "result")
    # print_data(data_dict)
    scatterplot(data_dict)

if __name__ == "__main__":
    main(sys.argv)
