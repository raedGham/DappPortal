# Generated by Django 5.0 on 2023-12-22 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_account_pofile_pic_account_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/photos/employee'),
        ),
    ]
