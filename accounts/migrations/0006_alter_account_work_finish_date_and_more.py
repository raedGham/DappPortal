# Generated by Django 5.0 on 2023-12-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='work_finish_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='work_start_date',
            field=models.DateField(null=True),
        ),
    ]
