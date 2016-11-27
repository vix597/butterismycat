'''
Views for comic app
'''

import random

from django.http import HttpResponse, Http404
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import Comic

def get_newest_comic():
    '''
    Get the newest comic if there is one
    '''
    try:
        return {'comic': Comic.objects.latest('pub_date')}
    except BaseException:
        return {'comic': None}

def get_oldest_comic():
    '''
    Get the oldest comic if there is one
    '''
    try:
        return {'comic': Comic.objects.order_by("pub_date")[0]} #puts oldest first
    except BaseException:
        return {'comic': None}

def get_comics(newest_first=False):
    '''
    Get all the comics in configurable order
    '''
    if newest_first:
        order_by = "-pub_date"
    else:
        order_by = "pub_date"

    try:
        return {'comics': Comic.objects.order_by(order_by)}
    except BaseException:
        return {'comics': []}

def get_comic_by_id(comic_id):
    '''
    Get comic by ID if it exists
    '''
    if not isinstance(comic_id, int):
        try:
            comic_id = int(comic_id)
        except ValueError:
            return {'comic': None}

    try:
        return {'comic': Comic.objects.get(id=comic_id)}
    except BaseException:
        return {'comic': None}

def get_next_comic(current_comic_id, newest_first=False):
    '''
    Used to get next or prev comic by changing 'newest_first' variable
    '''
    if newest_first:
        order_by = "-pub_date"
    else:
        order_by = "pub_date"

    if not isinstance(current_comic_id, int):
        try:
            current_comic_id = int(current_comic_id)
        except ValueError:
            return {'comic': None}

    try:
        comics = Comic.objects.order_by(order_by)
    except ObjectDoesNotExist:
        comics = []

    current_idx = None
    for idx, cur_comic in enumerate(comics):
        if cur_comic.id == current_comic_id:
            current_idx = idx
            break

    if current_idx is None:
        return {'comic': None}

    try:
        return {'comic': comics[current_idx + 1]}
    except IndexError:
        return {'comic': comics[current_idx]}

def index(request):
    '''
    Home page and load most recent comic
    '''
    template = loader.get_template('comic/index.html')
    context = get_newest_comic()
    return HttpResponse(template.render(context, request))

def archive(request):
    '''
    Comic archive
    '''
    template = loader.get_template('comic/archive.html')
    context = get_comics(newest_first=True)
    return HttpResponse(template.render(context, request))

def comic(request, comic_id):
    '''
    Permalink for a specific comic
    '''
    template = loader.get_template('comic/index.html')
    context = get_comic_by_id(comic_id)
    return HttpResponse(template.render(context, request))

def oldest(request):
    '''
    Get the oldest comic
    '''
    template = loader.get_template('comic/index.html')
    context = get_oldest_comic()
    return HttpResponse(template.render(context, request))

def next_comic(request, current_id):
    '''
    Get the next comic
    '''
    template = loader.get_template('comic/index.html')
    context = get_next_comic(current_id)
    return HttpResponse(template.render(context, request))

def prev_comic(request, current_id):
    '''
    Get the previous comic
    '''
    template = loader.get_template('comic/index.html')
    context = get_next_comic(current_id, newest_first=True) #switches it to get prev comic
    return HttpResponse(template.render(context, request))

def random_comic(request):
    '''
    Get a random comic
    '''
    random.seed(None) #Uses current system time
    r = random.randint(0, (Comic.objects.count() - 1))

    comics = get_comics()['comics']

    if len(comics) == 0:
        raise Http404("Cannot get random comic. No comics found.")

    try:
        rnd_comic = comics[r]
    except IndexError:
        rnd_comic = comics[0]

    template = loader.get_template('comic/index.html')
    context = {'comic': rnd_comic}
    return HttpResponse(template.render(context, request))
