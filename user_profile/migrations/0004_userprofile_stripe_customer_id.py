# Generated by Django 5.0.4 on 2024-05-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_remove_userprofile_city_remove_userprofile_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stripe_customer_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]