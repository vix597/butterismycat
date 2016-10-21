'''
JSON/Mongo config file classes
'''

class ConfigFile(object):
    '''
    Loads and saves a JSON formatted config file
    '''

    def __init__(self, path):
        pass

    def load(self):
        '''
        Load the config file from disk and parse JSON
        '''
        pass

    def save(self):
        '''
        Save the config file as JSON to disk
        '''
        pass

class MongoConfig(ConfigFile):
    '''
    Handles config values for a mongo DB connection
    '''

    def __init__(self, path, **kwargs):
        super(MongoConfig, self).__init__(path)
        self.database_name = kwargs.get("db", "butterismycat")



    