'''
ButterIsMyCat web server
'''

import os
from flask import Flask, g

APP = Flask(__name__)
APP.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

UPLOAD_FOLDER = os.path.join(APP.static_folder, "content")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

@APP.before_request
def global_before_request():
    '''
    Called before each web request.
    Don't put anything crazy in here
    '''
    g.upload_folder = UPLOAD_FOLDER
    g.allowed_extensions = ALLOWED_EXTENSIONS

def register_component(path):
    '''
    Register the views.py file inside web component folders
    '''

    import importlib
    views_path = path + '.views'
    module = importlib.import_module(views_path)
    APP.register_blueprint(module.BLUEPRINT)

# Load the views
register_component('butterismycat.ui.web.core')
register_component('butterismycat.ui.web.vendor')
register_component('butterismycat.ui.web.admin')

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
