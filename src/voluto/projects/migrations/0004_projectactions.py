# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20150922_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectActions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField(default=b'{}')),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
        ),
    ]
