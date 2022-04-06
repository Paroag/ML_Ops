from utils import merge_nested


def test_merge_nested():
    dic1 = {
        "A": 1,
        "B": 1,
        "D": {
            "DA": 1,
            "DB": 1,
        }
    }
    dic2 = {
        "A": 2,
        "C": 2,
        "D": {
            "DA": 2,
        }
    }

    assert merge_nested(dic1, dic2) == {
        "A": 2,
        "B": 1,
        "C": 2,
        "D": {
            "DA": 2,
            "DB": 1,
        }
    }
