# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abastece', '0006_auto_20161221_1827'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Punch',
        ),
        migrations.RenameField(
            model_name='base',
            old_name='coordX',
            new_name='coordx',
        ),
        migrations.RenameField(
            model_name='base',
            old_name='coordY',
            new_name='coordy',
        ),
        migrations.RenameField(
            model_name='posto',
            old_name='coordX',
            new_name='coordx',
        ),
        migrations.RenameField(
            model_name='posto',
            old_name='coordY',
            new_name='coordy',
        ),
        migrations.RenameField(
            model_name='tarefa',
            old_name='end_coordX',
            new_name='end_coordx',
        ),
        migrations.RenameField(
            model_name='tarefa',
            old_name='end_coordY',
            new_name='end_coordy',
        ),
        migrations.RenameField(
            model_name='tarefa',
            old_name='start_coordX',
            new_name='start_coordx',
        ),
        migrations.RenameField(
            model_name='tarefa',
            old_name='start_coordY',
            new_name='start_coordy',
        ),
        migrations.RenameField(
            model_name='viatura',
            old_name='coordX',
            new_name='coordx',
        ),
        migrations.RenameField(
            model_name='viatura',
            old_name='coordY',
            new_name='coordy',
        ),
        migrations.AddField(
            model_name='tarefa',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='base',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='modeloequipamento',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='modeloviatura',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='posto',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tipoevento',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='viatura',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
