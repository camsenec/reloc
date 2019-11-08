from django.contrib import admin

# Register your models here.
from .models import Area, Application, EdgeServer, Client


admin.site.register(Area)
admin.site.register(Application)
admin.site.register(EdgeServer)
admin.site.register(Client)
