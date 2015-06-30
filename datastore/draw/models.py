from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.conf import settings
from django.contrib.auth.models import User
import random
import string

def gen_ref():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))

class DrawManager(models.Manager):
    def get_by_natural_key(self, reference):
        return self.get(reference=reference)

class DrawCollection(models.Model):
    reference = models.CharField(max_length=10, unique=True, db_index=True, editable=False, default=gen_ref)
    date = models.DateField(auto_now_add=True)
    pathshp = models.FilePathField(path=settings.BASE_DIR + '/shapefile')
    status = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='draw', null=True)
    
    objects = DrawManager()
    
    class Meta:
        permissions = (
            ('view_draw', 'View draw'),
        )

class GeomDraw(models.Model):
    geom = models.GeometryField(srid=4326, spatial_index=True)
    metadata = HStoreField(default={'properties':'no properties'})
    draw = models.ForeignKey(DrawCollection, related_name='draw')
    owner = models.ForeignKey('auth.User', related_name='geom', null=True)
    objects = models.GeoManager()

    class Meta:
        permissions = (
            ('view_geom', 'View geom'),
        )

