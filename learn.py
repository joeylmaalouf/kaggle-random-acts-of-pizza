import json
import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns


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


def scatterplot(data, key1i, key2i, key3o):
    dataX = []
    dataY = []
    dataZ = []
    for d in data:
        dataX.append(float(d[key1i]))
        dataY.append(float(d[key2i]))
        dataZ.append(True if str(d[key3o]) == "True" else False)
    for i in range(len(dataX)):
        plt.plot(dataX[i], dataY[i], "." + ("g" if dataZ[i] else "r"))
    plt.show()


def main():
    # import JSON data as a list of dicts, each of which is a data point
    with open("train.json") as open_file:
        train = json.loads(unistring(open_file.read()))
#   print("account age      up - down    recieved pizza?")
#   for d in train:
#       print(relevant_data_string(d))
#       for k in d:
#           print(unistring(k), ":", unistring(d[k]), "\n")
    scatterplot(train, "requester_account_age_in_days_at_request",
                "requester_upvotes_minus_downvotes_at_request",
                "requester_received_pizza")


if __name__ == "__main__":
    main()
