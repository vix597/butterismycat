'''
Views for comic app
'''
import random
import logging

from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader

from .util import (
    get_newest_comic, get_comic_by_id, get_comics,
    get_next_comic, get_oldest_comic, get_is_oldest_newest
)
from .models import Comic

logger = logging.getLogger(__name__)


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
    newest_first = request.GET.get('newest_first', "true").lower().strip()
    if newest_first in ("true", "1", "yes", "on"):
        newest_first = True
    else:
        newest_first = False

    template = loader.get_template('comic/archive.html')
    context = get_comics(newest_first=newest_first)
    return HttpResponse(template.render(context, request))


def contact(request):
    '''
    Contact page
    '''
    template = loader.get_template('comic/contact.html')
    return HttpResponse(template.render(request=request))


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
    context = get_next_comic(current_id, newest_first=True)  # Switches it to get prev comic
    return HttpResponse(template.render(context, request))


def random_comic(request):
    '''
    Get a random comic
    '''
    context = {}
    r = random.randint(0, (Comic.objects.count() - 1))

    comics = get_comics()['comics']

    if not comics:
        raise Http404("Cannot get random comic. No comics found.")

    try:
        rnd_comic = comics[r]
    except IndexError:
        logger.error("random_comic() - Randomly selected an invalid index. Returning first comic.")
        rnd_comic = comics[0]

    # Update the number of views for the comic
    rnd_comic.num_views += 1
    rnd_comic.save()
    context['comic'] = rnd_comic
    context.update(get_is_oldest_newest(rnd_comic.id))

    template = loader.get_template('comic/index.html')
    return HttpResponse(template.render(context, request))
