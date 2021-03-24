# coding: utf-8
import requests

import pandas as pd
import numpy as np


def data_clean(data):
    for i in range(1, len(data.columns)):
        data = data[~data[data.columns[i]].isin(["None"])]
        data[data.columns[i]] = data[data.columns[i]].astype(np.float64)
    return data
# end

def get_parameter(data):
    res = data - 1.0
    res[res > 1] = 1.0
    res[res <= 1] = 0.8
    return 1 / res
# end

def create_feature_vector(data_list, data_type=["pm2.5", "pm10"], list_type="old"):
    feature_vectors = []

    for data in data_list:
        feature_vector = np.zeros((5,))
        df = data
        avg_fan = df["fan"].mean()

        for i in range(len(data_type)):
            sig = data[data_type[i] + "_pre"] - data[data_type[i] + "_post"]
            sig = sig[61:]
            mask = sig >= 0
            sig[mask] = (sig[mask] / data[data_type[i] + "_pre"]) * get_parameter(data[data_type[i] + "_pre"])
            sig[sig < 0] = 0
            sig = np.array(sig)

            feature_vector[0 + (2 * i)] = np.mean(sig)
            feature_vector[1 + (2 * i)] = np.std(sig)
        # end

        feature_vector[-1] = avg_fan
        feature_vectors.append(feature_vector)
    # end

    return feature_vectors
# end

class Filter_Clf:
    url = 'https://ffml.azurewebsites.net/predict'

    def __init__(self, log_name="./log.csv"):
        self.filename = log_name
    # end

    def update_filename(self, log_name):
        self.filename = log_name
    # end

    def predict(self):
        result = None
        data = pd.read_csv(self.filename)
        data = data_clean(data)
        data = create_feature_vector([data])
        payload = {"log": [data]}
        # print("Payload: {}".format(payload))

        response = requests.post(Filter_Clf.url, data=payload)

        if response.json() == None:
            print("Service Error. Return None.")
        else:
            # print(response.json())
            res = response.json()["prediction"]
            if res[0] == 1:
                print("Filter is working.")
                result = "Filter is working."
            elif res[0] == 0:
                print("Filter is not working.")
                result = "Filter is not working."
            else:
                print("Service Error.")
            # end
        # end

        return result
    # end
# end


# clf = Filter_Clf(log_name = "./2021-03-11_11_08_old.csv")
# clf.predict()
