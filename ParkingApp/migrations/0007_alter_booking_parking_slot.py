# Generated by Django 4.2.7 on 2023-11-13 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0006_remove_booking_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='parking_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParkingApp.parkingslot'),
        ),
    ]
