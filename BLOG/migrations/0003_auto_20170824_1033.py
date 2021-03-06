# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BLOG', '0002_blogpost_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='文章的类别名', max_length=100, unique=True, verbose_name='类别名称')),
            ],
        ),
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-date_added']},
        ),
    ]
