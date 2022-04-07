import json
import os

import pandas as pd
import tensorflow as tf

from ML_Ops import _FEATURES, _TARGET, _DATE, PROJECT_PATH
from utils import merge_nested


def get_merged_data(date: str = _DATE) -> dict:
    dic_data = {}
    for root, dirs, files in os.walk(f'./data/{date}/raw/'):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                dic_data = merge_nested(dic_data, json.loads(json.load(f))['data']['rates'])
    return dic_data


def get_dataframe(date: str = _DATE) -> pd.DataFrame:
    return pd.DataFrame.from_dict(get_merged_data(date), orient='index').dropna()


def get_dataset(date: str = _DATE) -> tf.data.Dataset:
    df = get_dataframe(date)
    df_features = df[_FEATURES]
    target = df.pop(_TARGET)
    return tf.data.Dataset.from_tensor_slices(
        (df_features, target)
    )


if __name__ == "__main__":
    print(get_dataframe().head(10))
    get_dataframe().to_csv(f"{PROJECT_PATH}/data/20220404/csv/data.csv", index=False)
    for feature_tensor, target_tensor in get_dataset():
        print(f'features:{feature_tensor} target:{target_tensor}')
