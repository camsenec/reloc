from django.contrib import admin

# Register your models here.
from .models import EdgeServer, Client


admin.site.register(EdgeServer)
admin.site.register(Client)
