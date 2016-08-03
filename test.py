# -*- coding: utf-8 -*-

import sqm

if __name__ == "__main__":
    f = open('data/mission.sqm')
    file_str = f.read()
    obj = sqm.decode(file_str)
    print "mission.sqm data: {}".format(str(obj))
