# Generated by Django 5.1 on 2024-11-01 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muna_kalati', '0006_rename_biref_description_openposition_brief_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
