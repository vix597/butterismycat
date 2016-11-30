'''
Models
'''

import datetime
from django.utils import timezone
from django.db import models

class Comic(models.Model):
    '''
    Database model for a comic strip
    '''
    image = models.ImageField(upload_to="comics/%Y/%m/%d")
    title = models.CharField(max_length=255, default="")
    show_title = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    hover_text = models.CharField(max_length=255, default="")
    include_hover_text = models.BooleanField(default=True)

    def was_published_recently(self):
        '''
        Returns if the comic was published in the last day
        '''
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return "{}".format(self.title)
