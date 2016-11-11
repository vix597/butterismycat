'''
Views for comic app
'''

#from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    '''
    Home page
    '''
    print("index(): ", request)
    return HttpResponse("Hello world")
