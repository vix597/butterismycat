'''
Tests the views
'''
import os
from pathlib import Path

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from comic.models import Comic


def create_comic(comic_title, hover_text):
    '''
    Creates a comic with the given title and hover text
    '''
    image_path = os.path.join(settings.MEDIA_ROOT, "tests", "test.png")
    image = SimpleUploadedFile(
        name='test.png',
        content=Path(image_path).read_bytes(),
        content_type='image/png'
    )
    return Comic.objects.create(title=comic_title, hover_text=hover_text, image=image)  # pylint: disable=E1101


class ComicViewTests(TestCase):
    '''
    Test all the comic views
    '''

    def test_comic_str(self):
        '''
        Test comic str() method
        '''
        comic = create_comic("Test", "Test Hover")
        self.assertEqual(str(comic), "Test")

    def test_index_view_with_no_comics(self):
        '''
        Test proper handling of an emtpy database on the index
        '''
        response = self.client.get(reverse('comic:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Could not find the requested comic")
        self.assertEqual(response.context['comic'], None)

    def test_archive_view_with_no_comics(self):
        '''
        Test proper handling of an empty database on the archive
        '''
        response = self.client.get(reverse('comic:archive'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, No comics")
        self.assertQuerysetEqual(response.context['comics'], [])
        self.assertEqual(len(response.context['comics']), 0)

    def test_index_with_comic(self):
        '''
        Test proper handling of index with comic
        '''
        create_comic("Test 1", "Test 1 hover")
        response = self.client.get(reverse('comic:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test 1")
        self.assertContains(response, "Test 1 hover")
        self.assertEqual(str(response.context['comic']), 'Test 1')

    def test_archive_with_comics(self):
        '''
        Test proper handling of archive with some comics
        '''
        create_comic("Test 1", "Test 1 hover")
        create_comic("Test 2", "Test 2 hover")
        response = self.client.get(reverse('comic:archive'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test 1")
        self.assertContains(response, "Test 2")
        self.assertQuerysetEqual(
            response.context['comics'],
            ['<Comic: Test 2>', '<Comic: Test 1>']
        )

    def test_permalink_with_no_comic(self):
        '''
        Test proper handling of a broken permalink
        '''
        response = self.client.get(reverse('comic:permalink', kwargs={"comic_id": 0}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Could not find the requested comic")
        self.assertEqual(response.context['comic'], None)

    def test_permalink_with_comic(self):
        '''
        Test proper handling of permalink with a comic
        '''
        c = create_comic("Test 1", "Test 1 hover")
        response = self.client.get(reverse('comic:permalink', kwargs={"comic_id": c.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test 1")
        self.assertContains(response, "Test 1 hover")
        self.assertEqual(str(response.context['comic']), 'Test 1')
