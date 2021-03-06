# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abastece', '0002_linhabase_posto_ok'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cronograma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrada', models.DateField()),
                ('preventiva', models.DateField(null=True)),
                ('asbuilt', models.DateField(null=True)),
                ('plano_verao', models.DateField(null=True)),
                ('preditiva', models.DateField(null=True)),
                ('retirada58', models.DateField(null=True)),
                ('antena915', models.DateField(null=True)),
                ('sinal', models.DateField(null=True)),
                ('outro', models.DateField(null=True)),
                ('icr', models.DateField(null=True)),
                ('suporte_angular', models.DateField(null=True)),
                ('posto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='abastece.Posto')),
            ],
        ),
    ]
