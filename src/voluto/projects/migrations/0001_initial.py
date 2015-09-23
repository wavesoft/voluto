# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import voluto.projects.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=voluto.projects.models.new_uuid, help_text=b'Project identification string', unique=True, max_length=32, db_index=True)),
                ('name', models.CharField(default=b'', help_text=b'The name of this project', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(default=1, help_text=b'Project files revision number')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'PE', help_text=b'Current status of the project files', max_length=2, choices=[(b'PE', b'Available'), (b'ST', b'Staging'), (b'PU', b'Published'), (b'RE', b'Retired')])),
                ('src', models.CharField(default=b'', help_text=b'The URL where the files can be obtained from', max_length=4096)),
                ('url', models.CharField(default=None, max_length=4096, null=True, help_text=b'The URL where the files are available at', blank=True)),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='files',
            field=models.ForeignKey(related_name='projectfiles', default=None, blank=True, to='projects.ProjectFiles', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
