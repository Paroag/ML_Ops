import copy


def merge_nested(dic1: dict, dic2: dict) -> dict:
    new_dic = copy.deepcopy(dic1)
    for key, value in dic2.items():
        if key not in dic1.keys():
            new_dic[key] = value
        elif not isinstance(dic1[key], dict):
            if isinstance(value, dict):
                raise ValueError("int/str value should not be overridden with dictionary")
            elif not isinstance(value, dict):
                new_dic[key] = value
        elif isinstance(dic1[key], dict):
            if not isinstance(value, dict):
                raise ValueError("dict should not be overridden with int/str value")
            elif isinstance(value, dict):
                new_dic[key] = merge_nested(dic1[key], dic2[key])

    return new_dic
