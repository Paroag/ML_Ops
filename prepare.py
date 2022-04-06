import json
import os

import pandas as pd
import tensorflow as tf

from utils import merge_nested

_DATE = "20220404"
_FEATURES = ["RUB"]
_TARGET = "WHEAT"


def get_merged_data(date: str = _DATE) -> dict:
    dic_data = {}
    for root, dirs, files in os.walk(f'./data/{date}/raw/'):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                dic_data = merge_nested(dic_data, json.loads(json.load(f))['data']['rates'])
    return dic_data


def get_dataframe(date: str = _DATE) -> pd.DataFrame:
    return pd.DataFrame.from_dict(get_merged_data(date), orient='index')


def get_dataset(date: str = _DATE) -> tf.data.Dataset:
    df = get_dataframe(date)
    df_features = df[_FEATURES]
    target = df.pop(_TARGET)
    return tf.data.Dataset.from_tensor_slices(
        (df_features, target)
    )
