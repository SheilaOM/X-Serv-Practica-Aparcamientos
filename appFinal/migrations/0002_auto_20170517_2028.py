# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleccionado',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='letra',
            field=models.IntegerField(default=0),
        ),
    ]
