# -*- coding: utf-8 -*-


def encode_sqm(data_dict):
    # Some simplest cases first:
    if data_dict is None or type(data_dict) is not dict:
        raise TypeError
    if data_dict == {}:
        return ""

    data_str = ""

    # version attribute must be first, I think
    ordered_keys = ['version']

    for key in ordered_keys:
        if key in data_dict:
            data_str = dump_pair(key, data_dict[key], data_str)

    for key in data_dict:
        if key not in ordered_keys:
            data_str = dump_pair(key, data_dict[key], data_str)

    return data_str


def dump_pair(key, value, data_str):
    if type(value) == str:
        data_str = dump_string(key, value, data_str)
    else:
        data_str = dump_number(key, value, data_str)
    return data_str


def dump_string(key, value, data_str):
    data_str += "{}=\"{}\";\n".format(key, value)
    return data_str


def dump_number(key, value, data_str):
    data_str += "{}={};\n".format(key, value)
    return data_str


'''Tests'''

if __name__ == '__main__':

    from bcolors import print_result


    def test_encode_wrong_data():
        data_dict = "{}"

        try:
            encoded_str = encode_sqm(data_dict)
        except TypeError:
            print "test_encode_wrong_data -> True: TypeError raised."
        else:
            print_result("test_encode_wrong_data -> False: TypeError not raised. Returned \"{}\"".format(encoded_str),
                         False)


    def test_encode_empty():
        data_dict = {}
        data_str = ""

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result("test_encode_empty -> {}: \"{}\" == \"{}\"".format(success, encoded_str, data_str), success)


    def test_encode_attribute_string():
        data_dict = {
            'some_stuff': "\"Important\" Data",
        }
        data_str = "some_stuff=\"\"\"Important\"\" Data\";"

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result("test_encode_attribute_string -> {}: {} == {}".format(success, encoded_str, data_str), success)


    def test_encode_attribute_int():
        data_dict = {
            'version': 52,
        }
        data_str = "version=52;"

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result("test_encode_attribute_int -> {}: {} == {}".format(success, encoded_str, data_str), success)


    def test_encode_attribute_float():
        data_dict = {
            'atlOffset': 3.1415,
        }
        data_str = "atlOffset=3.1415;"

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result("test_encode_attribute_float -> {}: {} == {}".format(success, encoded_str, data_str), success)


    def test_encode_attribute_float_exp():
        data_dict = {
            'atlOffset': -4.7683716e-07,
        }
        data_str = "atlOffset=-4.7683716e-007;"  # TODO: not so sure

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result("test_encode_attribute_float_exp -> {}: {} == {}".format(success, encoded_str, data_str), success)


    test_encode_wrong_data()
    test_encode_empty()
    test_encode_attribute_string()
    test_encode_attribute_int()
    test_encode_attribute_float()
    test_encode_attribute_float_exp()
