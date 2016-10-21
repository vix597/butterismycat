'''
Classes for communicating with MongoDB server
'''

class Mongo(object):
    '''
    Connects to MongoDB/Creates the DB/and handles insert/update/etc...
    '''

    def __init__(self, cfg):
        self.cfg = cfg
