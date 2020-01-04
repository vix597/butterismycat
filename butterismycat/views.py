'''
Views for comic app
'''
import os

from django.views.static import serve

from .settings import MEDIA_ROOT


def serve_comic_image(request, year, month, day, filename):
    '''
    Serve the actual comic image file
    '''
    file_path = os.path.join("comics", year, month, day, filename)
    return serve(request, file_path, document_root=MEDIA_ROOT, show_indexes=False)
