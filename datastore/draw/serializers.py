from django.forms import widgets
from rest_framework import serializers
from draw.models import DrawCollection

class DrawCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawCollection
        fields = ('reference','date')