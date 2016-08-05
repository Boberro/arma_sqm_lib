# -*- coding: utf-8 -*-

import sqm

if __name__ == "__main__":
    def test_decoder():
        f = open('data/mission.sqm')
        file_str = f.read()
        obj = sqm.decode(file_str)
        print "test_decoder --> mission.sqm data: {}".format(str(obj))
        return obj


    def test_encoder(obj):
        data_str = sqm.encode(obj)
        print "test_encoder --> re-encoded .sqm: {}".format(data_str)


    print "\n"
    data = test_decoder()
    print "\n"
    test_encoder(data)
