# Generated by Django 4.2.7 on 2023-11-12 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0005_alter_booking_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='modified',
        ),
    ]