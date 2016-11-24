'''
Views for comic app
'''

from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Comic

def index(request):
    '''
    Home page and load most recent comic
    '''
    try:
        latest_comic = Comic.objects.latest('pub_date')
    except ObjectDoesNotExist:
        latest_comic = None

    template = loader.get_template('comic/index.html')
    context = {
        'comic': latest_comic
    }

    return HttpResponse(template.render(context, request))

def archive(request):
    '''
    Comic archive
    '''
    try:
        comics = Comic.objects.order_by('-pub_date') # Puts the newest first
    except ObjectDoesNotExist:
        comics = []

    template = loader.get_template('comic/archive.html')
    context = {
        'comics': comics
    }

    return HttpResponse(template.render(context, request))

def comic(request, comic_id):
    '''
    Permalink for a specific comic
    '''
    try:
        permalink_comic = Comic.objects.get(id=comic_id)
    except ObjectDoesNotExist:
        permalink_comic = None

    template = loader.get_template('comic/index.html')
    context = {
        'comic': permalink_comic
    }

    return HttpResponse(template.render(context, request))

def oldest(request):
    '''
    Get the oldest comic
    '''
    try:
        oldest_comic = Comic.objects.order_by('pub_date')
    except ObjectDoesNotExist:
        oldest_comic = None

    template = loader.get_template('comic/index.html')
    context = {
        'comic': oldest_comic
    }

    return HttpResponse(template.render(context, request))

def next(request, current_id):
    '''
    Get the next comic
    '''
    pass

def prev(request, current_id):
    '''
    Get the previous comic
    '''
    pass

def random(request):
    '''
    Get a random comic
    '''
    pass
