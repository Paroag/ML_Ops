import datetime
import json
import os

import requests

START_DATE = "2022-04-02"
END_DATE = "2022-04-06"
COMMODITIES = ["WHEAT", "USD", "RUB"]


def create_url_from_parameters(
        endpoint: str,
        parameters: dict,
) -> str:
    return f"{endpoint}?{'&'.join(f'{key}={value}' for key, value in parameters.items())}"


def get_raw_data(
        endpoint=None,
        parameters=None
) -> requests.Response:
    parameters = parameters if parameters is not None else {}
    if "access_key" not in parameters.keys():
        parameters = {**parameters, **{"access_key": "uxg52jj8d009vim9i3gd4538cy96kansupjtrum2qth3w0xv64kg2h8q6sq3"}}
    return requests.get(
        create_url_from_parameters(endpoint=endpoint, parameters=parameters)
    )


if __name__ == '__main__':
    now_str = datetime.datetime.now().strftime("%Y%m%d")
    try:
        os.mkdir(f"./data/{now_str}")
    except FileExistsError:
        pass

    time_series_endpoint = "https://www.commodities-api.com/api/timeseries"

    for commodity in COMMODITIES:
        time_series_parameters = {
            "start_date": START_DATE,
            "end_date": END_DATE,
            "symbols": commodity,
            "base": "EUR",
        }
        response = get_raw_data(
            endpoint=time_series_endpoint,
            parameters=time_series_parameters,
        )
        a = json.loads(response.content)
        with open(f"./data/{now_str}/raw/{commodity}.json", "w") as f:
            json.dump(json.dumps(a), f)
        with open(f"./data/{now_str}/info.txt", "a") as f:
            f.write(create_url_from_parameters(endpoint=time_series_endpoint, parameters=time_series_parameters) + "\n")
