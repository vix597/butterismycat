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

    def __str__(self):
        return "{}".format(self.title)
