# Generated by Django 5.1 on 2024-11-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muna_kalati', '0007_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
