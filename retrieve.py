import datetime
import json
import os

import requests


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
    """
    https://www.commodities-api.com/api/timeseries
    ? access_key = API_KEY
    & start_date = 2012-05-01
    & end_date = 2012-05-25
    """

    raise NotImplemented("must change API requests")

    now_str = datetime.datetime.now().strftime("%Y%m%d")
    os.mkdir(f"./data/{now_str}")

    for commodity in ["WHEAT", "RUB"]:
        response = get_raw_data(
            endpoint="https://www.commodities-api.com/api/timeseries",
            parameters={
                'start_date': '2021-04-15',
                'end_date': '2022-04-01',
                'symbols': commodity,
                'base': 'EUR',
            }
        )
        a = json.loads(response.content)
        with open(f'./data/{now_str}/{commodity}.json', 'w') as f:
            json.dump(json.dumps(a), f)
