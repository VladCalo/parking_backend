# Generated by Django 4.2.7 on 2024-01-07 12:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ParkingApp", "0002_booking_modified_alter_booking_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="modified",
        ),
    ]