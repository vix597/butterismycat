'''
Views for comic app
'''

from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Comic

def index(request):
    '''
    Home page
    '''
    latest_comic = Comic.objects.latest('pub_date')
    template = loader.get_template('comic/index.html')
    context = {
        'comic': latest_comic
    }

    return HttpResponse(template.render(context, request))

def archive(request):
    '''
    Comic archive
    '''
    comics = Comic.objects.order_by('-pub_date') # Puts the newest first
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
