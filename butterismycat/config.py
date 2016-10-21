

class ConfigFile(object):
    '''
    Loads and saves a JSON formatted config file
    '''

    def __init__(self, path):
        pass

    def load(self):
        pass

    def save(self):
        pass

class MongoConfig(ConfigFile):

    def __init__(self, path, **kwargs):
        super(MongoConfig, self).__init__(path)
