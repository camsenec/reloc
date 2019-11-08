from rest_framework import serializers
from .models import EdgeServer, Client


class EdgeServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeServer
        fields = ('x','y', 'capacity', 'remain', 'clients')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('x','y')


'''
class ManyItemsSerializer(serializers.Serializer):

    """ All 'Item' Model serialize. """
    items = SpinGlassFieldSerializer(many=True, allow_null=True, default=SpinGlassField.objects.all())
'''
