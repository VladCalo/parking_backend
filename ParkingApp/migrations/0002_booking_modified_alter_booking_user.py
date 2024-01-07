# Generated by Django 4.2.7 on 2024-01-07 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ParkingApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="modified",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="booking",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="ParkingApp.users"
            ),
        ),
    ]