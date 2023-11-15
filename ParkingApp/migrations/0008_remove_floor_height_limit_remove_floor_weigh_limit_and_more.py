# Generated by Django 4.2.7 on 2023-11-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0007_alter_booking_parking_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='floor',
            name='height_limit',
        ),
        migrations.RemoveField(
            model_name='floor',
            name='weigh_limit',
        ),
        migrations.AddField(
            model_name='parkdetails',
            name='height_limit',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='parkdetails',
            name='weigh_limit',
            field=models.IntegerField(default=3500),
        ),
    ]
