# Generated by Django 4.2.7 on 2024-02-24 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medreps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medrep',
            name='first_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_approval_medreps', to=settings.AUTH_USER_MODEL),
        ),
    ]