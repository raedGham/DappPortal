# Generated by Django 5.0 on 2024-01-03 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0003_alter_vacation_ampm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='nodays',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]
