# Generated by Django 5.0.4 on 2024-05-29 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_venuemanager_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='about',
            field=models.TextField(default='About', max_length=1500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='desc',
            field=models.CharField(max_length=300),
        ),
    ]
