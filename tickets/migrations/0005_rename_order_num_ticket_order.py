# Generated by Django 5.0.4 on 2024-05-30 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticketorder_order_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='order_num',
            new_name='order',
        ),
    ]
