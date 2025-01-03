# Generated by Django 5.1.2 on 2024-10-31 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profesores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('profesores', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profesores.profesor')),
            ],
        ),
    ]
