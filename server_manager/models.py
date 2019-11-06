from django.db import models

# Create your models here.

class Client(models.Model):
    #id = models.AutoField(primary_key=True)
    x = models.FloatField()
    y = models.FloatField()

class EdgeServer(models.Model):
    #id = models.AutoField(primary_key=True)
    x = models.FloatField()
    y = models.FloatField()
    capacity = models.FloatField()
    remain = models.FloatField()
    clients = models.ManyToManyField(Client)

    
