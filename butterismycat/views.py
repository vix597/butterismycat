'''
Main views for the website. Redirects to comic app
'''

from django.shortcuts import redirect

def index(_): #Passing _ variable to avoid linting warning
    '''
    Redirect to comic
    '''
    return redirect("/comic/", permanent=True)
