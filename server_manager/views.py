from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import EdgeServer, Client
from django.db.models import Q, Max
from .serializer import EdgeServerSerializer, ClientSerializer

from strategy import allocator

from rest_framework.decorators import list_route

# Create your views here.

class EdgeServerViewSet(viewsets.ModelViewSet):
    queryset = EdgeServer.objects.all()
    serializer_class = EdgeServerSerializer

    @list_route(methods=["post"])
    def post(self, requeset):
        application_id = request.POST['application_id'] #シミュレーター上では指定
        server_id = EdgeServer.objects.raw('SELECT MAX(server_id) FROM edge_server') + 1 #server_idは各アプリケーションで指定
        x = request.POST['x']
        y = request.POST['y']
        capacity = request.POST['capacity']

        server = EdgeServer.objects.create(application_id = applicatin_id, server_id = server_id, x = x, y = y, capacity = capacity, remain = capacity)
        server.save()
        return Response(status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def get(self, request):
        application_id = request.GET["application_id"]
        server_id = request.GET["server_id"]
        server = self.queryset.get(Q(application_id = application_id), Q(server_id = server_id))
        serializer = self.get_serializer(server)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)



#クライアントサイドのアプリケーションから呼び出されるAPI
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @list_route(methods=["post"])
    def post(self, request):
        application_id = request.POST['application_id'] #シミュレーター上では指定
        client_id = Client.objects.all().aggregate(Max('client_id'))['client_id__max'] + 1
        print('client_id', client_id)
        x = request.POST['x']
        y = request.POST['y']

        client = Client.objects.create(application_id = application_id, client_id = client_id, x = x, y = y)
        client.save()

        serializer = self.get_serializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=["get"])
    def get(self, request, pk = None):
        application_id = request.GET["application_id"]
        client_id = request.GET["client_id"]
        client = self.queryset.get(Q(application_id = application_id), Q(client_id = client_id))
        serializer = self.get_serializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        clients = Client.objects.all()
        serializer = self.get_serializer(clients, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=["put"])
    def update_home_server(self, request):
        application_id = request.GET["application_id"]
        client_id = request.GET["client_id"]
        client = self.queryset.get(Q(application_id = application_id), Q(client_id = client_id))

        #application_idの指定により, 領域の大きさ（Kの大きさ）をテーブルより取得
        #一旦ランダムに配置
        new_home_server_id = server_clustering(application_id, client_id)
        client.home = EdgeServer.objects.get(client_id = new_home_server_id)
