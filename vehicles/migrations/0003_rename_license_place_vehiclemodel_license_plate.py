# Generated by Django 3.2.2 on 2021-05-26 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_rename_licence_place_vehiclemodel_license_place'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiclemodel',
            old_name='license_place',
            new_name='license_plate',
        ),
    ]
