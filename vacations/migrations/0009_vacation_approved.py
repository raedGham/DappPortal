# Generated by Django 5.0 on 2024-01-15 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0008_vacation_first_app_status_vacation_fourth_app_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacation',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]