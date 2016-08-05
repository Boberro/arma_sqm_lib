# -*- coding: utf-8 -*-


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def print_result(result_str, result):
    if result:
        print result_str
    else:
        print FAIL + result_str + ENDC
