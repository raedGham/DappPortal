# Generated by Django 5.0 on 2023-12-24 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_account_work_finish_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='profile_pic',
        ),
    ]
