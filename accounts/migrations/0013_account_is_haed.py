# Generated by Django 5.0 on 2024-01-15 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_account_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_haed',
            field=models.BooleanField(default=False),
        ),
    ]
