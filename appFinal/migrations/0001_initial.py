# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamiento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=60)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('descripcion', models.TextField()),
                ('accesible', models.IntegerField()),
                ('barrio', models.CharField(max_length=20)),
                ('distrito', models.CharField(max_length=20)),
                ('url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('texto', models.TextField()),
                ('aparcamiento', models.ForeignKey(to='appFinal.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='DatosContacto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('telefono', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('claseVia', models.CharField(max_length=10)),
                ('nombreVia', models.TextField()),
                ('numero', models.CharField(max_length=8)),
                ('localidad', models.CharField(max_length=20)),
                ('provincia', models.CharField(max_length=20)),
                ('cp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Seleccionado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('aparcamiento', models.ForeignKey(to='appFinal.Aparcamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=32)),
                ('tituloPag', models.CharField(max_length=32)),
                ('letra', models.IntegerField()),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='seleccionado',
            name='usuario',
            field=models.ForeignKey(to='appFinal.Usuario'),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='datosContacto',
            field=models.ForeignKey(to='appFinal.DatosContacto'),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='direccion',
            field=models.ForeignKey(to='appFinal.Direccion'),
        ),
    ]
