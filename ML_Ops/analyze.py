import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from ML_Ops.modeling import create_model


def reformat_as_time_series(dic: dict, commodities_name: str):
    return (
        np.array(
            [
                datetime.strptime(date, "%Y-%m-%d")
                for date in dic["data"]["rates"].keys()
            ]
        ),
        np.array(
            [
                1/values[commodities_name]
                for date, values in dic["data"]["rates"].items()
            ]
        )
    )


def get_common(reformat1, reformat2):
    l1 = []
    l2 = []
    for index, date in enumerate(reformat1[0]):
        if date in reformat2[0]:
            l1.append(reformat1[1][index])
            l2.append(reformat2[1][list(reformat2[0]).index(date)])
    return np.array(l1), np.array(l2)


def plot(reformat_data1, reformat_data2):
    ax1 = plt.subplot()
    l1, = ax1.plot(reformat_data1[0], reformat_data1[1], color='yellow')
    ax2 = ax1.twinx()
    l2, = ax2.plot(reformat_data2[0], reformat_data2[1], color='red')
    plt.legend([l1, l2], ["wheat", "rub"])
    plt.show()


def plot_scatter(reformat_data1, reformat_data2):
    plt.scatter(*get_common(reformat_data1, reformat_data2))
    plt.show()


def display_all(date):
    with open(f"../data/{date}/raw/WHEAT.json", "r") as f:
        wheat_data = json.loads(json.load(f))
    with open(f"../data/{date}/raw/RUB.json", "r") as f:
        rub_data = json.loads(json.load(f))
    wheat_reformat_data = reformat_as_time_series(wheat_data, commodities_name="WHEAT")
    rub_reformat_data = reformat_as_time_series(rub_data, commodities_name="RUB")
    plot(wheat_reformat_data, rub_reformat_data)
    plot_scatter(wheat_reformat_data, rub_reformat_data)


if __name__ == "__main__":

    DATE = "20220407"
    # display_all(DATE)

    """import tensorflow as tf
    keras_model = tf.keras.models.load_model("../tmp/1649337448/")"""
    keras_model = create_model()
    keras_model.summary()
    tmp = np.array([
        [0.1],
        [1]
    ])
    print(tmp.shape)
    print(
        keras_model.predict(tmp)
    )
