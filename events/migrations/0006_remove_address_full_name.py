# Generated by Django 5.0.4 on 2024-05-07 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_venuemanager_venue_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='full_name',
        ),
    ]