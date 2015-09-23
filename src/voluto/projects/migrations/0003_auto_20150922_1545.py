# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_projectfiles_filetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('level', models.IntegerField(default=0, choices=[(0, b'Info'), (1, b'Warning'), (2, b'Error'), (3, b'Critical')])),
                ('text', models.CharField(default=b'', max_length=1024)),
                ('project', models.ForeignKey(to='projects.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='projectfiles',
            name='status',
            field=models.CharField(default=b'PE', help_text=b'Current status of the project files', max_length=2, choices=[(b'PE', b'Pending'), (b'ST', b'Staging'), (b'PU', b'Published'), (b'RE', b'Retired')]),
        ),
    ]
