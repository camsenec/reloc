from django.db import models

# Create your models here.

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
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 128)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class EdgeServer(models.Model):
    class Meta:
        unique_together = (('server_id', 'application_id'))

    application_id = models.IntegerField(default=0)
    server_id = models.IntegerField(default=0)
    x = models.FloatField()
    y = models.FloatField()
    capacity = models.FloatField()
    remain = models.FloatField()
    cluster_id = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)

class Client(models.Model):
    class Meta:
        unique_together = (('client_id', 'application_id'))

    application_id = models.IntegerField(default=0)
    client_id = models.IntegerField(default=0)
    x = models.FloatField()
    y = models.FloatField()
    home = models.ForeignKey(EdgeServer, on_delete=models.CASCADE, blank = True, null = True)
    #EdgeServerにClientがぶら下がる
    #serverを外部キーにして参照

    def __str__(self):
        return str(self.id)

'''
Yser
friends = ForeignKey(FRIENDS)

review は wineにぶら下がっている
reviewのところにwineをforeign keyとして背負う

同様に, client, edgeserverのところにapplicationをforeign keyとして背負う
違う, 多対多の関係
edgeserverは, 多くのアプリケーションを管理する
Application
'''
