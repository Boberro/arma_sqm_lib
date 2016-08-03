# -*- coding: utf-8 -*-
import re


FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
R_WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

R_ATTRIBUTE = re.compile(r'(\w+)(?:[ \t\n\r]*)=')
R_ATTRIBUTE_LIST = re.compile(r'(\w+)\[\](?:[ \t\n\r]*)=[ \t\n\r]*\{', FLAGS)
R_CLASS = re.compile(r'class(?:[ \t\n\r]+)(\w+)(?:[ \t\n\r]+)\{', FLAGS)

R_NUMBER = re.compile(r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?(?:;|,)?')
R_STRING = re.compile(r'\"(.+)?\"(?:;|,)?')


def scan_sqm(string):
    idx = R_WHITESPACE.match(string, 0).end()

    data = {}
    while idx < len(string):
        name, value, idx = scan_pair(string, idx)
        if name is not None:
            data[name] = value
        else:
            raise StopIteration
    return data


def scan_pair(string, idx):
    match = R_ATTRIBUTE.match(string, idx)
    attribute_type = 'value'
    if match is None:
        match = R_ATTRIBUTE_LIST.match(string, idx)
        attribute_type = 'list'
    if match is None:
        match = R_CLASS.match(string, idx)
        attribute_type = 'class'

    if match is not None:
        (attribute,) = match.groups()
        idx = R_WHITESPACE.match(string, match.end()).end()
        value, idx = scan_value(string, attribute_type, idx)
        idx = R_WHITESPACE.match(string, idx).end()
        return attribute, value, idx
    else:
        raise StopIteration


def scan_value(string, type, idx):
    if type == 'value':
        next_char = string[idx]
        if next_char == '"':
            match = R_STRING.match(string, idx)
            if match is not None:
                (string_value,) = match.groups()
                return parse_string(string_value), match.end()
        else:
            match = R_NUMBER.match(string, idx)
            if match is not None:
                integer, fraction, exp = match.groups()
                return parse_number(integer, fraction, exp), match.end()
    elif type == 'list':
        return parse_list(string, idx)
    elif type == 'class':
        return parse_class(string, idx)
    else:
        raise StopIteration


def parse_string(string):
    return string  # TODO: might not work for code


def parse_number(integer, fraction, exp):
    if fraction or exp:
        res = float(integer + (fraction or '') + (exp or ''))
    else:
        res = int(integer)
    return res


def parse_list(string, idx):
    _list = []

    end_list = False
    while not end_list:
        next_char = string[idx]
        if next_char == '}' and string[idx:idx+2] == '};':
            idx += 2
            end_list = True
        else:
            value, idx = scan_value(string, 'value', idx)
            _list.append(value)
            idx = R_WHITESPACE.match(string, idx).end()

    return _list, idx


def parse_class(string, idx):
    _dict = {}

    end_dict = False
    while not end_dict:
        next_char = string[idx]
        if next_char == '}' and string[idx:idx + 2] == '};':
            idx += 2
            end_dict = True
        else:
            name, value, idx = scan_pair(string, idx)
            if name is not None:
                _dict[name] = value
            else:
                raise StopIteration

    return _dict, idx


# TESTS

if __name__ == '__main__':

    def test_attribute():
        file_data = {
            'version': 10,
            'author': "Unknown",
            'pi': 3.14,
        }

        # region Generate String
        file_str = ''
        for key in file_data:
            if type(file_data[key]) == str:
                file_str += "{}=\"{}\";\n".format(key, file_data[key])
            else:
                file_str += "{}={};\n".format(key, file_data[key])
        # endregion

        obj = scan_sqm(file_str)
        print "test_attribute: {} is equal {} ?  ->  {}".format(str(obj), str(file_data), obj == file_data)


    def test_list():
        file_str1 = '''list1[]={1,"2",3};'''
        file_str2 = '''list1[]=
        {
        1,
        "2",
        3
        };'''

        file_data = {
            "list1": [1, "2", 3]
        }

        obj = scan_sqm(file_str1)
        print "test_list: {} is equal {} ?  ->  {}".format(str(obj), str(file_data), obj == file_data)

        obj = scan_sqm(file_str2)
        print "test_list: {} is equal {} ?  ->  {}".format(str(obj), str(file_data), obj == file_data)


    def test_class():
        file_str = '''class foo
        {
            sna="fu";

            class bar
            {
                foobar=1;
            };
        };'''
        file_data = {
            "foo": {
                "sna": "fu",
                "bar": {
                    "foobar": 1
                }
            }
        }
        obj = scan_sqm(file_str)
        print "test_class: {} is equal {} ?  ->  {}".format(str(obj), str(file_data), obj == file_data)


    test_attribute()
    test_list()
    test_class()
