# Generated by Django 5.0 on 2024-01-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0004_alter_vacation_nodays'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeleavestat',
            name='description',
            field=models.CharField(default='', max_length=50),
        ),
    ]
