# Generated by Django 4.2.7 on 2024-02-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_account_is_guard'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='has_med_ent',
            field=models.BooleanField(default=False),
        ),
    ]