# Generated by Django 5.0 on 2024-01-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_account_address_alter_account_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/photos/employee'),
        ),
    ]
