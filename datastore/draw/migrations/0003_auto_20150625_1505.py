# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import draw.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('draw', '0002_auto_20150625_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawcollection',
            name='owner',
            field=models.ForeignKey(related_name='draw', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='geomdraw',
            name='owner',
            field=models.ForeignKey(related_name='geom', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='drawcollection',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='drawcollection',
            name='reference',
            field=models.CharField(default=draw.models.gen_ref, unique=True, max_length=10, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='drawcollection',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='geomdraw',
            name='draw',
            field=models.ForeignKey(related_name='draw', to='draw.DrawCollection'),
        ),
    ]
