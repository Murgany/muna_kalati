# Generated by Django 5.1 on 2025-01-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muna_kalati', '0016_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(choices=[(3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'), (5.0, '5.0')], decimal_places=1, max_digits=2),
        ),
    ]
