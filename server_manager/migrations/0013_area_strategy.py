# Generated by Django 3.1.6 on 2021-03-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_manager', '0012_delete_strategy'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='strategy',
            field=models.CharField(default='RLCCA', max_length=120),
        ),
    ]
