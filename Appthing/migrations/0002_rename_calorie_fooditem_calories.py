# Generated by Django 4.1 on 2022-09-01 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Appthing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fooditem',
            old_name='calorie',
            new_name='calories',
        ),
    ]
