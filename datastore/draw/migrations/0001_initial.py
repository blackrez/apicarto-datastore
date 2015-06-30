# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reference', models.CharField(unique=True, max_length=10, editable=False, db_index=True)),
                ('date', models.DateField()),
                ('pathshp', models.FilePathField(path=b'/home/nabil/studio/apicarto-datastore/datastore/shapefile')),
            ],
        ),
        migrations.CreateModel(
            name='GeomDraw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poly', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('metadata', django.contrib.postgres.fields.hstore.HStoreField(default={b'properties': b'no properties'})),
                ('draw', models.ForeignKey(to='draw.Draw')),
            ],
        ),
    ]
