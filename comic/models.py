'''
Models
'''

import datetime
from django.utils import timezone
from django.db import models

class Comic(models.Model):
    '''
    Database model for a comic strip
    @image - The comic image to upload. Uploded to MEDIA_ROOT/comics/<year>/<month>/<day>
    @hover_text - Text to display on mouse over
    @title - The title of the comic
    @pub_date - The date the comic was uploaded to the site
    '''
    image = models.ImageField(upload_to="comics/%Y/%m/%d")
    title = models.CharField(max_length=255, default="")
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    hover_text = models.CharField(max_length=255, default="")

    def was_published_recently(self):
        '''
        Returns if the comic was published in the last day
        '''
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return "{}".format(self.title)
