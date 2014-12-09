import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys


def unistring(s):
    """Encodes our Unicode string to ASCII, then back to Unicode.
    In the translation, we ignore all unknown characters, which removes
    all of the non-ASCII characters that break our string parsing.
    """
    return str(s).encode("ascii", "ignore").decode()


def process_data(data_json, key1, renamed1, key2, renamed2, key3, renamed3,
                 key4, renamed4, key5, renamed5, key6, renamed6):
    """Converts our list of dictionaries to a dictionary of lists,
    while processing some of the data points (e.g. converting number strings
    to ints and float, as well as lowercasing strings). Also uses renamed keys
    instead of the very long default ones.
    """
    val1 = []
    val2 = []
    val3 = []
    val4 = []
    val5 = []
    val6 = []
    for d in data_json:
        val1.append(d[key1])
        val2.append(float(d[key2]))
        val3.append(int(d[key3]))
        val4.append(d[key4].lower())
        val5.append(d[key5].lower())
        val6.append(str(d[key6]) == "true" or str(d[key6]) == "True")
    return {renamed1: val1,
            renamed2: val2,
            renamed3: val3,
            renamed4: val4,
            renamed5: val5,
            renamed6: val6}


def get_best_fit_poly(data_dict, x, y, deg):
    """Finds the coefficients of the polynomial function for the best fit line.
    """
    coeffs = np.polyfit(x=data_dict[x], y=data_dict[y], deg=deg)
    return np.poly1d(coeffs)


def scatterplot(data_dict):
    """Visualizes account age versus karma on the x and y axes, and whether
    or not the requester was given a pizza as the green or red point color.
    """
    for i in range(len(data_dict["age"])):
        formatting = "." + ("g" if data_dict["result"][i] else "r")
        plt.plot(data_dict["age"][i], data_dict["karma"][i], formatting)
    poly = get_best_fit_poly(data_dict, "age", "karma", 1)
    plt.plot(data_dict["age"], poly(data_dict["age"]))
    plt.show()


def will_reciprocate(data_dict, index):
    """Searches the text of the request for phrases that suggest a promise to
    give pizza to someone else. data_dict is a dictionary of lists,and any given
    index in the lists corresponds to the same post for different keys.
    """
    title = data_dict["title"][index]
    body = data_dict["body"][index]
    phrases = ["pay it forward", "return the favor", "reciprocate"]
    for p in phrases:
        if p in title or p in body:
            return True
    return False


def print_data(data_dict):
    """Prints the data for examining or debugging purposes.
    """
    print("id, age, karma, reciprocal, result")
    for i in range(len(data_dict["id"])):
        print(
            data_dict["id"][i],
            data_dict["age"][i],
            data_dict["karma"][i],
            will_reciprocate(data_dict, i),
            data_dict["result"][i]
        )


def main(argv):
    """The main program itself. Imports JSON data as a list of dictionaries,
    each of which is a data point (a pizza request). Then makes predictions
    as to whether or not the request would be fulfilled based on whether or
    not they offered to reciprocate, as well as whether or not they had more
    karma than the corresponding point on the best-fit line.
    """
    with open("train.json") as open_file:
        train = json.loads(unistring(open_file.read()))
    data_dict = process_data(train,
                             "request_id",
                             "id",
                             "requester_account_age_in_days_at_request",
                             "age",
                             "requester_upvotes_minus_downvotes_at_request",
                             "karma",
                             "request_title",
                             "title",
                             "request_text_edit_aware",
                             "body",
                             "requester_received_pizza",
                             "result")
    # print_data(data_dict)
    # scatterplot(data_dict)
    poly = get_best_fit_poly(data_dict, "age", "karma", 1)
    predictions = [(poly(data_dict["age"][i]) < data_dict["karma"][i])
                   or will_reciprocate(data_dict, i)
                   for i in range(len(data_dict["id"]))]
    with open("predictions.csv", "w") as output:
        output.write("request_id,requester_received_pizza\n")
        for i in range(len(data_dict["id"])):
            output.write("%s,%d\n" % (data_dict["id"][i], predictions[i]))


if __name__ == "__main__":
    main(sys.argv)
