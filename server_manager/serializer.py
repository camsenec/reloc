from rest_framework import serializers
from .models import EdgeServer, Client


class EdgeServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeServer
        fields = ('application_id', 'server_id', 'x','y', 'capacity', 'remain')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('application_id', 'client_id', 'x', 'y')


'''
class ManyItemsSerializer(serializers.Serializer):

    """ All 'Item' Model serialize. """
    items = SpinGlassFieldSerializer(many=True, allow_null=True, default=SpinGlassField.objects.all())
'''
