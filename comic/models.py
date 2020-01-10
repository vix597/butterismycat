'''
Models
'''
import datetime
from django.utils import timezone
from django.db import models
from django import forms


class Comic(models.Model):
    '''
    Database model for a comic strip
    '''
    #: Image file to upload to the site.
    image = models.ImageField(verbose_name='Image', upload_to="comics/%Y/%m/%d")

    #: Title of the comic
    title = models.CharField(verbose_name='Title', max_length=512, blank=True)

    #: Whether or not to display the title
    show_title = models.BooleanField(
        verbose_name='Show Title', default=True,
        help_text='If this is checked, the title of the comic will be displayed on the web page. Uncheck to hide the title for this comic.')

    #: Date and time it was published
    pub_date = models.DateTimeField(verbose_name='Date Published', auto_now_add=True)

    #: The text displayed when the user's mouse hovers over the comic
    hover_text = models.TextField(verbose_name='Hover Text', max_length=1024, blank=True)

    #: Whether or not to include the hover text in the page.
    include_hover_text = models.BooleanField(
        verbose_name='Include Hover Text', default=True,
        help_text='If this is checked, the hover text will be displayed when the user hovers their mouse over the comic. Uncheck to disable hover text for this comic.')

    #: A description for the comic. This can be longer.
    description = models.TextField(verbose_name='Description', max_length=10000, blank=True)

    #: Whether or not the description should be exposed for this comic
    show_description = models.BooleanField(
        verbose_name='Show Description', default=False,
        help_text='If this is checked, the description will be accessible for this comic. Leave this unchecked to keep the description private.')

    #: Number of times the comic has been loaded
    num_views = models.IntegerField(verbose_name='Number of Views', default=0)

    #: Total number of shares accross all social media
    num_shares = models.IntegerField(verbose_name='Number of Social Media Shares', default=0)

    #: Whether the comic is or is not safe for work
    is_nsfw = models.BooleanField(verbose_name="Is Not Safe For Work?", default=False,
        help_text="If this is checked, the comic is NSFW and will be hidden by default. The user will need to click to reveal the comic.")

    def __str__(self):
        return "{}".format(self.title)
