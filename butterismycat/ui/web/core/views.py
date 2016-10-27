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

    return render_template("/core/index.html", num_comics=0)

@BLUEPRINT.route('/content')
def most_recent():
    '''
    Return the most recent comic
    '''
    return {}

@BLUEPRINT.route('/content/<index>')
def specific():
    '''
    Return a specific comic
    '''
    return {}
