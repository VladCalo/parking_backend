# Generated by Django 4.2.7 on 2023-11-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0003_alter_credentials_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingslot',
            name='physical_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parkingslot',
            name='standard_price',
            field=models.IntegerField(default=10),
        ),
    ]
