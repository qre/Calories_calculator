# Generated by Django 4.1 on 2022-09-05 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appthing', '0006_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('bread', 'bread, cereal'), ('meat', 'meat, fish'), ('fruits', 'fruits, vegetables'), ('milk', 'milk, dairy'), ('fats', 'fats, sugars')], max_length=50),
        ),
    ]
