# Generated by Django 4.2.7 on 2023-11-12 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='booking',
            table='Booking',
        ),
        migrations.AlterModelTable(
            name='floor',
            table='Floor',
        ),
        migrations.AlterModelTable(
            name='park',
            table='Park',
        ),
        migrations.AlterModelTable(
            name='parkdetails',
            table='ParkingDetails',
        ),
        migrations.AlterModelTable(
            name='parkingslotrules',
            table='ParkingSlotRules',
        ),
        migrations.AlterModelTable(
            name='parkowner',
            table='ParkOwner',
        ),
        migrations.AlterModelTable(
            name='users',
            table='Users',
        ),
    ]
