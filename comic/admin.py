'''
Admin interface for our comic site
'''
from django.contrib import admin
from .models import Comic

admin.site.register(Comic)
