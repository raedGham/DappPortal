# Generated by Django 5.0 on 2024-01-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overtime',
            name='to_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
