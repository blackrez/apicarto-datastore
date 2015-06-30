import geojson
from django.contrib.gis.geos import GEOSGeometry
from .models import DrawCollection, GeomDraw

from django.conf import settings


#django rest
from rest_framework import renderers
from .serializers import DrawCollectionSerializer
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.core.serializers import serialize


#Export shapefile
import shapefile
import os
import zipfile
import StringIO
import glob
from django.http import HttpResponse


from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def store(request):
    if request.method == 'GET':
        draws = DrawCollection.objects.filter(owner=request.user)
        serializer = DrawCollectionSerializer(draws, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        geojson_draw = request.DATA.get('geojson')
        print(request.DATA)
        print(request.DATA.get('geojson'))
        print type(geojson_draw)
        geojson_loaded = geojson.loads(geojson_draw)

        d = DrawCollection.objects.create(status=False, owner=request.user)
        d.save()
        print type(geojson_loaded)
        if type(geojson_loaded) == geojson.FeatureCollection:
            for feature in geojson_loaded.get('features'):
                print(feature)
                geom = GEOSGeometry(feature.get('geometry').__str__())
                g = GeomDraw.objects.create(geom=geom, metadata=feature.properties, draw=d, owner=request.user)
                g.save()
            d.status = True
            d.save()
        elif type(geojson_loaded) == geojson.Feature:
            geom = GEOSGeometry(geojson_loaded.get('geometry').__str__())
            g = GeomDraw.objects.create(geom=geom, metadata=geojson_loaded.properties, draw=d, owner=request.user)
            g.save()
            d.status = True
            d.save()
        else:
            return Response({'status':'not supported, use Feature ou FeatureCollection'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'reference':d.reference}, status=status.HTTP_201_CREATED)


class GeoJsonRenderer(renderers.BaseRenderer):
    media_type = 'application/json'
    format = 'json'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

@api_view()
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def detail(request, reference):
    draws = DrawCollection.objects.filter(reference=reference).first()
    if draws == None:
         return Response({}, status=status.HTTP_404_NOT_FOUND)
    if request.GET.get('export') == 'shapefile':
        #TODO make tasks!
        path = "{0}/shapefile/{1}".format(settings.BASE_DIR, draws.reference)

        w = shapefile.Writer()
        for g in draws.draw.all():
            w.poly(parts=map(list,g.geom.tuple))
            for key in g.metadata.keys():
                print(key)
                w.field(str(key), 'C', 40)
            print(g.metadata.values())
            w.record(*g.metadata.values())
        
        w.save(path)
        s = StringIO.StringIO()
        zip_filename = draws.reference + '.zip'
        zf = zipfile.ZipFile(s, "w")

        filenames =  glob.glob(path + '.*')
        for fpath in filenames:
            print fpath
            zf.write(fpath, os.path.join(draws.reference,os.path.basename(fpath)))
        zf.close()


        resp = HttpResponse(s.getvalue())
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp
    else:
        features = serialize('geojson', draws.draw.all(), fields=('draw', 'metadata', 'geom'))
        return HttpResponse(features, content_type="application/json")
