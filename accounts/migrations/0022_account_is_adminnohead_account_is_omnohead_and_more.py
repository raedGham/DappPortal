# Generated by Django 5.0 on 2024-02-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_account_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_AdminNoHead',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_OMnoHead',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_OMwithHead',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_deputy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='is_engineer',
            field=models.BooleanField(default=False),
        ),
    ]
