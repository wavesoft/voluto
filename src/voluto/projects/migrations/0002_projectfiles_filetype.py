# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfiles',
            name='filetype',
            field=models.CharField(default=b'', help_text=b'The type of the project files', max_length=5, choices=[(b'zip', b'.zip file'), (b'tgz', b'.tar.gz file'), (b'tbz2', b'.tar.bz2 file'), (b'txz', b'.tar.xz file'), (b'git', b'GIT Repository'), (b'svn', b'SVN Repository'), (b'cvmfs', b'CVMFS Link')]),
        ),
    ]
