# Generated by Django 3.0.2 on 2020-01-11 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='comics/%Y/%m/%d', verbose_name='Image')),
                ('title', models.CharField(blank=True, max_length=512, verbose_name='Title')),
                ('show_title', models.BooleanField(default=True, help_text='If this is checked, the title of the comic will be displayed on the web page. Uncheck to hide the title for this comic.', verbose_name='Show Title')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Published')),
                ('hover_text', models.TextField(blank=True, max_length=1024, verbose_name='Hover Text')),
                ('include_hover_text', models.BooleanField(default=True, help_text='If this is checked, the hover text will be displayed when the user hovers their mouse over the comic. Uncheck to disable hover text for this comic.', verbose_name='Include Hover Text')),
                ('description', models.TextField(blank=True, max_length=10000, verbose_name='Description')),
                ('show_description', models.BooleanField(default=False, help_text='If this is checked, the description will be accessible for this comic. Leave this unchecked to keep the description private.', verbose_name='Show Description')),
                ('num_views', models.IntegerField(default=0, verbose_name='Number of Views')),
                ('is_nsfw', models.BooleanField(default=False, help_text='If this is checked, the comic is NSFW and will be hidden by default. The user will need to click to reveal the comic.', verbose_name='Is Not Safe For Work?')),
            ],
        ),
    ]
