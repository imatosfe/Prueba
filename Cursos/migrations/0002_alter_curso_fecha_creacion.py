# Generated by Django 5.1.2 on 2024-11-08 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='fecha_creacion',
            field=models.DateField(),
        ),
    ]
