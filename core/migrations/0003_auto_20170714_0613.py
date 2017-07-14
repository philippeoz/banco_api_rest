# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_caixa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caixa',
            name='cedula_cem',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='cedula_cinco',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='cedula_cinquenta',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='cedula_dez',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='cedula_dois',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='cedula_um',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='cedula_vinte',
            field=models.IntegerField(default=0),
        ),
    ]
