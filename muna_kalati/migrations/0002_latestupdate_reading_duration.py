# Generated by Django 5.1 on 2024-09-22 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muna_kalati', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='latestupdate',
            name='reading_duration',
            field=models.CharField(default='5 minutes', max_length=20),
        ),
    ]
