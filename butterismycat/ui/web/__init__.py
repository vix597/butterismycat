'''
ButterIsMyCat web server
'''

from flask import Flask, g

APP = Flask(__name__)

@APP.before_request
def global_before_request():
    '''
    Called before each web request.
    Don't put anything crazy in here
    '''
    g.db = None

def register_component(path):
    '''
    Register the views.py file inside web component folders
    '''

    import importlib
    views_path = path + '.views'
    module = importlib.import_module(views_path)
    APP.register_blueprint(module.blueprint)

# Load the views
register_component('butterismycat.core')
register_component('butterismycat.vendor')

def run(debug=False, port=5001):
    '''
    Run the server.
    If debug, run the builtin flask APP server
    Else, run the production ready tornado server
    '''

    if debug:
        APP.run(debug=debug, host="localhost", port=port)
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(APP))
        http_server.listen(port, address="0.0.0.0")
        IOLoop.instance().start()
