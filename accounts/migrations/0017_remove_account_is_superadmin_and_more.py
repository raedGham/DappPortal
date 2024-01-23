# Generated by Django 5.0 on 2024-01-18 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_account_groups_account_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_superadmin',
        ),
        migrations.AlterField(
            model_name='account',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]