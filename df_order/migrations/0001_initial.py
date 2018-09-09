# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('odata', models.DateTimeField(auto_now_add=True)),
                ('oIsPay', models.BooleanField(default=True)),
                ('otatal', models.DecimalField(max_digits=6, decimal_places=2)),
                ('user', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
    ]
