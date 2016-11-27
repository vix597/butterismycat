'''
Views for comic app
'''

import random

from django.http import HttpResponse, Http404
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
        oldest_comic = Comic.objects.order_by('pub_date')[0]
    except ObjectDoesNotExist:
        oldest_comic = None

    template = loader.get_template('comic/index.html')
    context = {
        'comic': oldest_comic
    }

    return HttpResponse(template.render(context, request))

def next_comic(request, current_id):
    '''
    Get the next comic
    '''
    try:
        comics = Comic.objects.order_by("pub_date")
    except ObjectDoesNotExist:
        comics = []

    try:
        current_id = int(current_id)
    except ValueError:
        raise Http404("Invalid value passed as the current comic ID")

    current_idx = None
    for idx, cur_comic in enumerate(comics):
        if cur_comic.id == current_id:
            current_idx = idx
            break

    if current_idx is None:
        raise Http404("Error retrieving next comic. Current comic not found.")

    try:
        nxt_comic = comics[current_idx + 1]
    except IndexError:
        nxt_comic = comics[current_idx]

    template = loader.get_template('comic/index.html')
    context = {
        'comic': nxt_comic
    }

    return HttpResponse(template.render(context, request))

def prev_comic(request, current_id):
    '''
    Get the previous comic
    '''
    try:
        comics = Comic.objects.order_by("-pub_date")
    except ObjectDoesNotExist:
        comics = []

    try:
        current_id = int(current_id)
    except ValueError:
        raise Http404("Invalid value passed as the current comic ID")

    current_idx = None
    for idx, cur_comic in enumerate(comics):
        if cur_comic.id == current_id:
            current_idx = idx
            break

    if current_idx is None:
        raise Http404("Error retrieving previous comic. Current comic not found.")

    try:
        prv_comic = comics[current_idx + 1]
    except IndexError:
        prv_comic = comics[current_idx]

    template = loader.get_template('comic/index.html')
    context = {
        'comic': prv_comic
    }

    return HttpResponse(template.render(context, request))

def random_comic(request):
    '''
    Get a random comic
    '''
    random.seed(None) #Uses current system time
    r = random.randint(0, (Comic.objects.count() - 1))

    try:
        comics = Comic.objects.order_by("-pub_date")
    except ObjectDoesNotExist:
        comics = []

    if len(comics) == 0:
        raise Http404("Cannot get random comic. No comics found.")

    try:
        rnd_comic = comics[r]
    except IndexError:
        rnd_comic = comics[0]

    template = loader.get_template('comic/index.html')
    context = {
        'comic': rnd_comic
    }

    return HttpResponse(template.render(context, request))
