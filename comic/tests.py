'''
Tests
'''

import datetime
import os

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Comic

class ComicMethodTests(TestCase):
    '''
    Test the comic model methods
    '''

    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() should return False for comics whose
        pub_date is in the future.
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Comic(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() should return False for comics whose
        pub_date is older than 1 day.
        '''
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Comic(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() should return True for comics whose
        pub_date is within the last day.
        '''
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Comic(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_comic(comic_title, hover_text):
    '''
    Creates a comic with the given title and hover text
    '''
    image_path = os.path.join(settings.MEDIA_ROOT, "tests", "test.jpg")
    image = SimpleUploadedFile(
        name='test.jpg',
        content=open(image_path, 'rb').read(),
        content_type='image/jpeg'
    )
    return Comic.objects.create(title=comic_title, hover_text=hover_text, image=image)

class ComicViewTests(TestCase):
    '''
    Test all the comic views
    '''

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
        response = self.client.get(reverse('comic:permalink', kwargs={"comic_id":0}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Could not find the requested comic")
        self.assertEqual(response.context['comic'], None)

    def test_permalink_with_comic(self):
        '''
        Test proper handling of permalink with a comic
        '''
        c = create_comic("Test 1", "Test 1 hover")
        response = self.client.get(reverse('comic:permalink', kwargs={"comic_id":c.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test 1")
        self.assertContains(response, "Test 1 hover")
        self.assertEqual(str(response.context['comic']), 'Test 1')
