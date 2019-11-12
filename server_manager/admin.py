from django.contrib import admin

# Register your models here.
from .models import Cluster, Area, Application, EdgeServer, Client


admin.site.register(Cluster)
admin.site.register(Area)
admin.site.register(Application)
admin.site.register(EdgeServer)
admin.site.register(Client)
