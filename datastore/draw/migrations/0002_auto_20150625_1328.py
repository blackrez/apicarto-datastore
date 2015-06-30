# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference', models.CharField(unique=True, max_length=10, editable=False, db_index=True)),
                ('date', models.DateField()),
                ('pathshp', models.FilePathField(path=b'/home/nabil/studio/apicarto-datastore/datastore/shapefile')),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.RenameField(
            model_name='geomdraw',
            old_name='poly',
            new_name='geom',
        ),
        migrations.AlterField(
            model_name='geomdraw',
            name='draw',
            field=models.ForeignKey(to='draw.DrawCollection'),
        ),
        migrations.DeleteModel(
            name='Draw',
        ),
    ]
