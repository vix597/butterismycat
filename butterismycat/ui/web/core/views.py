'''
Core view
'''

from flask import render_template, Blueprint

BLUEPRINT = Blueprint('core', __name__)

@BLUEPRINT.route('/')
def index():
    '''
    Load index.html
    '''

    return render_template("/core/index.html")
