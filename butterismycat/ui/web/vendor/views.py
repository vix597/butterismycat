'''
Vendor views module. Used to get web components from the bower_components
directory
'''

import os
from flask import Blueprint, send_from_directory, abort
from werkzeug.utils import secure_filename

BOWER_COMPONENTS = os.path.abspath(os.path.join(__file__, "..", "..", "bower_components"))

BLUEPRINT = Blueprint('vendor', __name__, url_prefix="/vendor")

@BLUEPRINT.route("/<path:filename>")
def serve(filename):
    '''
    Serve web components inside the bower_components directory if the
    url_prefix is /vendor
    '''

    print("BOWER_COMPONENTS: ", BOWER_COMPONENTS)
    print("Serve: ", filename)

    if '..' in filename:
        abort(404)

    filename = secure_filename(filename)

    return send_from_directory(BOWER_COMPONENTS, filename)
