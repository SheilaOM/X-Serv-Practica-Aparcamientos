# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0003_aparcamiento_numcoments'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
    ]
