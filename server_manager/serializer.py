from rest_framework import serializers
from .models import SpinGlassField


class EdgeServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeServer
        fields = ('x','y', 'capacity', 'remain', 'clients')


'''
class ManyItemsSerializer(serializers.Serializer):

    """ All 'Item' Model serialize. """
    items = SpinGlassFieldSerializer(many=True, allow_null=True, default=SpinGlassField.objects.all())
'''
