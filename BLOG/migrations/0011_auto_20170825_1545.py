# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BLOG', '0010_auto_20170825_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, to='BLOG.Tag'),
        ),
    ]
