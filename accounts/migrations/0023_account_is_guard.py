# Generated by Django 5.0 on 2024-02-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_account_is_adminnohead_account_is_omnohead_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_guard',
            field=models.BooleanField(default=False),
        ),
    ]