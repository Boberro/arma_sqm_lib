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
            data_str = dump_pair(key, data_dict[key])

    for key in data_dict:
        if key not in ordered_keys:
            data_str = dump_pair(key, data_dict[key])

    return data_str


def dump_pair(key, value, depth=0):
    if type(value) == dict:
        key_str = "class {}".format(key)
    elif type(value) == list:
        key_str = "{}[]=".format(key)
    else:
        key_str = "{}=".format(key)

    def do_inline():
        if depth == 0 \
                and type(value) == list \
                and key in ['addons']:
            return False
        return True

    inline = do_inline()

    value_str = dump_value(value, depth=depth, inline=inline)
    return '{}{};\n'.format(key_str, value_str)


def dump_value(value, depth=0, inline=True):
    if type(value) == dict:
        value_str = dump_class(value, depth=depth)
    elif type(value) == list:
        value_str = dump_list(value, inline=inline)
    elif type(value) == str:
        value_str = dump_string(value)
    else:
        value_str = dump_number(value)
    return value_str


def dump_string(value):
    value_enc = value.replace('"', '""')
    return '"{}"'.format(value_enc)


def dump_number(value):
    return str(value)


def dump_list(value, inline=True):
    value_enc = '{'
    l = len(value)
    for i in range(l):
        if not inline and i == 0:
            value_enc += '\n\t'
        value_enc += dump_value(value[i])
        if i < l - 1:
            value_enc += ','
        if not inline:
            value_enc += '\n'
            if i < l - 1:
                value_enc += '\t'
    value_enc += '}'
    return value_enc


def dump_class(obj, depth=0):
    if not obj:
        return ' {}'

    depth_str = ''
    for i in range(depth):
        depth_str += '\t'

    value_enc = '\n' + depth_str + '{\n'
    for key in obj:
        value_enc += depth_str + '\t' + dump_pair(key, obj[key], depth=depth + 1)
    value_enc += depth_str + '}'

    return value_enc


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
            print_result('test_encode_wrong_data -> False: TypeError not raised. Returned "{}"'.format(encoded_str),
                         False)


    def test_encode_empty():
        data_dict = {}
        data_str = ""

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_empty -> {}: "{}" == "{}"'.format(success, encoded_str, data_str), success)


    def test_encode_attribute_string():
        data_dict = {
            'some_stuff': '"Important" Data',
        }
        data_str = 'some_stuff="""Important"" Data";'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_attribute_string -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_attribute_int():
        data_dict = {
            'version': 52,
        }
        data_str = "version=52;"

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_attribute_int -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_attribute_float():
        data_dict = {
            'atlOffset': 3.1415,
        }
        data_str = "atlOffset=3.1415;"

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_attribute_float -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_attribute_float_exp():
        data_dict = {
            'atlOffset': -4.7683716e-07,
        }
        data_str = "atlOffset=-4.7683716e-007;"  # TODO: not so sure

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_attribute_float_exp -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_list_empty():
        data_dict = {
            'list0': [],
        }
        data_str = "list0[]={};"

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_list_empty -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_list_of_string():
        data_dict = {
            'list1': ["a", "b", "c"],
        }
        data_str = 'list1[]={"a","b","c"};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_list_of_string -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_list_of_numbers():
        data_dict = {
            'list2': [1, 2, 3.1415],
        }
        data_str = 'list2[]={1,2,3.1415};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_list_of_numbers -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_list_of_addons():
        data_dict = {
            'addons': ["a", "b", "c"],
        }
        data_str = 'addons[]={\n\t"a",\n\t"b",\n\t"c"\n};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_list_of_addons -> {}: {} == {}\n'.format(success, encoded_str, data_str), success)


    def test_encode_class_empty():
        data_dict = {
            'Class0': {},
        }
        data_str = 'class Class0 {};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_class_empty -> {}: {} == {}'.format(success, encoded_str, data_str), success)


    def test_encode_class_with_attribute():
        data_dict = {
            'Class1': {
                'value1': 1,
            },
        }
        data_str = 'class Class1\n{\n\tvalue1=1;\n};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_class_with_attribute -> {}:{} == {}\n'.format(success, encoded_str, data_str),
                     success)


    def test_encode_class_with_list():
        data_dict = {
            'Class2': {
                'addons': [1, 2, 3, 4, 5],
            },
        }
        data_str = 'class Class2\n{\n\taddons[]={1,2,3,4,5};\n};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_class_with_list -> {}:{} == {}\n'.format(success, encoded_str, data_str),
                     success)


    def test_encode_class_with_class_with_attribute():
        data_dict = {
            'Class3': {
                'Class4': {
                    'value': 15,
                },
            },
        }
        data_str = 'class Class3\n{\n\tclass Class4\n\t{\n\t\tvalue=15;\n\t};\n};'

        encoded_str = (encode_sqm(data_dict)).strip()
        success = (encoded_str == data_str)
        print_result('test_encode_class_with_list -> {}: "{}" == "{}"\n'.format(success, encoded_str, data_str),
                     success)


    test_encode_wrong_data()
    test_encode_empty()
    test_encode_attribute_string()
    test_encode_attribute_int()
    test_encode_attribute_float()
    test_encode_attribute_float_exp()
    test_encode_list_empty()
    test_encode_list_of_string()
    test_encode_list_of_numbers()
    test_encode_list_of_addons()
    test_encode_class_empty()
    test_encode_class_with_attribute()
    test_encode_class_with_list()
    test_encode_class_with_class_with_attribute()
