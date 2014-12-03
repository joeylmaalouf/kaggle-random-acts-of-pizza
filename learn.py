import json


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


def main():
    # import JSON data as a list of dicts, each of which is a data point
    with open("train.json") as open_file:
        train = json.loads(unistring(open_file.read()))
    print("account age      up - down    recieved pizza?")
    for d in train:
        print(relevant_data_string(d))
    #   for k in d:
    #       print(unistring(k), ":", unistring(d[k]), "\n")


if __name__ == "__main__":
    main()
