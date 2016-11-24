# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-11 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='hover_text',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='comic',
            name='image',
            field=models.ImageField(upload_to='comics/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]