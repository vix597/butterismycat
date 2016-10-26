'''
Vendor views module. Used to get web components from the bower_components
directory
'''

import os
from flask import Blueprint, send_from_directory, abort
from werkzeug.urls import url_fix

BOWER_COMPONENTS = os.path.abspath(os.path.join(__file__, "..", "..", "bower_components"))

BLUEPRINT = Blueprint('vendor', __name__, url_prefix="/vendor")

@BLUEPRINT.route("/<path:filename>")
def serve(filename):
    '''
    Serve web components inside the bower_components directory if the
    url_prefix is /vendor
    '''

    if '..' in filename:
        abort(404)

    safe_url = url_fix(filename)

    return send_from_directory(BOWER_COMPONENTS, safe_url)
