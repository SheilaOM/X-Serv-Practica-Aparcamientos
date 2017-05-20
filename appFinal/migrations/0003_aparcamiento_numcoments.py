# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFinal', '0002_auto_20170517_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='numComents',
            field=models.IntegerField(default=0),
        ),
    ]
