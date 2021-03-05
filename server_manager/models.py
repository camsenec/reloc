from django.db import models

# Create your models here.

class Cluster(models.Model):
    application_id = models.IntegerField()
    cluster_id = models.IntegerField()
    centroid_x = models.FloatField()
    centroid_y = models.FloatField()

    def __str__(self):
        return str(self.cluster_id)


class Area(models.Model):
    SIZE_CHOICES = (
        (1, "SMALL"),
        (2, "MEDIUM"),
        (3, "BIG"),
    )
    size = models.IntegerField(choices= SIZE_CHOICES)
    avg_n_cooperative_server = models.IntegerField()

    def __str__(self):
        return str(self.size);

class Application(models.Model):
    application_id = models.IntegerField(default=1)
    name = models.CharField(max_length = 128)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default = 1)

    def __str__(self):
        return str(self.id)

class EdgeServer(models.Model):
    class Meta:
        unique_together = (('server_id', 'application_id'))

    application_id = models.IntegerField(default=1)
    server_id = models.IntegerField(default=1)

    x = models.FloatField()
    y = models.FloatField()
    capacity = models.FloatField()
    used = models.FloatField()
    connection = models.IntegerField(default=0)
    cp = models.FloatField(default=0)
    cluster_id = models.IntegerField(default=1)

    def __str__(self):
        return str(self.server_id)

class Client(models.Model):
    class Meta:
        unique_together = (('client_id', 'application_id'))

    application_id = models.IntegerField(default=1)
    client_id = models.IntegerField(default=1)

    x = models.FloatField()
    y = models.FloatField()
    home = models.ForeignKey(EdgeServer, on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return str(self.client_id)
