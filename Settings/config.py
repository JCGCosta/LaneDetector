import os

class Common(object):
    COLOR_SELECTION = os.getenv('DISTANCES', '-1')

class Dev(Common):
    pass

class Production(Common):
    pass