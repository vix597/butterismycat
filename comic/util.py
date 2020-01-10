'''
Helpful utilities for butterismycat comic app
'''
import logging
from enum import Enum

from django.core.exceptions import ObjectDoesNotExist

from .models import Comic

logger = logging.getLogger(__name__)


def get_is_oldest_newest(current_comic_id):
    '''
    Get a dict containing the updated values of is_oldest and is_newest
    for the current comic ID.
    '''
    ret = {
        'is_oldest': False,
        'is_newest': False
    }

    try:
        oldest_comic = Comic.objects.order_by("pub_date")[0]  # Puts oldest first
        newest_comic = Comic.objects.latest('pub_date')
    except Exception as e:
        logger.exception("get_is_oldest_newest() - Failed: %s", str(e))
        return ret

    if oldest_comic.id == current_comic_id:
        ret["is_oldest"] = True
    if newest_comic.id == current_comic_id:
        ret["is_newest"] = True

    return ret


def get_newest_comic():
    '''
    Get the newest comic if there is one
    '''
    try:
        comic = Comic.objects.latest('pub_date')
        comic.num_views += 1
        comic.save()
        return {
            'comic': comic,
            'is_oldest': False,
            'is_newest': True
        }
    except Exception as e:
        logger.exception("get_newest_comic() - Failed: %s", str(e))
        return {'comic': None}


def get_oldest_comic():
    '''
    Get the oldest comic if there is one
    '''
    try:
        comic = Comic.objects.order_by("pub_date")[0]  # Puts oldest first
        comic.num_views += 1
        comic.save()
        return {
            'comic': comic,
            'is_oldest': True,
            'is_newest': False
        }
    except Exception as e:
        logger.exception("get_oldest_comic() - Failed: %s", str(e))
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
    except Exception as e:
        logger.exception("get_comics() - Failed: %s", str(e))
        return {'comics': []}


def get_comic_by_id(comic_id):
    '''
    Get comic by ID if it exists
    '''
    ret = {}

    if comic_id is None:
        return {'comic': None}

    if not isinstance(comic_id, int):
        try:
            comic_id = int(comic_id)
        except ValueError:
            logger.error("get_comic_by_id() - Integer is required for comic ID.")
            return {'comic': None}

    try:
        comic = Comic.objects.get(id=comic_id)
        comic.num_views += 1
        comic.save()
        ret['comic'] = comic
        ret.update(get_is_oldest_newest(comic.id))
        return ret
    except Exception as e:
        logger.exception("get_comic_by_id() - Failed: %s", str(e))
        return {'comic': None}


def get_next_comic(current_comic_id, newest_first=False):
    '''
    Used to get next or prev comic by changing 'newest_first' variable
    '''
    ret = {}

    if current_comic_id is None:
        return {'comic': None}

    if newest_first:
        order_by = "-pub_date"
    else:
        order_by = "pub_date"

    if not isinstance(current_comic_id, int):
        try:
            current_comic_id = int(current_comic_id)
        except ValueError:
            logger.error("get_next_comic() - Integer is required for comic ID.")
            return {'comic': None}

    try:
        comics = Comic.objects.order_by(order_by)
    except ObjectDoesNotExist:
        logger.debug("get_next_comic() - This must be the last comic. No next comic.")
        comics = []

    current_idx = None
    for idx, cur_comic in enumerate(comics):
        if cur_comic.id == current_comic_id:
            current_idx = idx
            break

    if current_idx is None:
        logger.error("get_next_comic() - Error: Could not find current comic in site.")
        return {'comic': None}

    try:
        comic = comics[current_idx + 1]
        comic.num_views += 1
        comic.save()
        ret['comic'] = comic
        ret.update(get_is_oldest_newest(comic.id))
        return ret
    except IndexError:
        logger.error("get_next_comic() - Error: No next comic in result array.")
        comic = comics[current_idx]
        comic.num_views += 1
        comic.save()
        ret['comic'] = comic
        ret.update(get_is_oldest_newest(comic.id))
        return ret
