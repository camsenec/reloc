from rest_framework import serializers
from .models import EdgeServer, Client, Cluster


class EdgeServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeServer
        fields = ('application_id', 'server_id', 'x','y', 'capacity', 'used', 'cluster_id')

class ClientSerializer(serializers.ModelSerializer):
    #下記に定義するメソッド経由
    home = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('application_id', 'client_id', 'x', 'y', 'home')

    #インスタンスとは, clientインスタンスを指している
    def get_home(self, instance):
        return str(instance.home.server_id)

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('application_id', 'cluster_id', 'centroid_x','centroid_y')



'''
class ManyItemsSerializer(serializers.Serializer):

    """ All 'Item' Model serialize. """
    items = SpinGlassFieldSerializer(many=True, allow_null=True, default=SpinGlassField.objects.all())
'''
