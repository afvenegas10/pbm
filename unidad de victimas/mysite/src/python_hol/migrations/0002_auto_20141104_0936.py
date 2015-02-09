# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_hol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RDominio',
            fields=[
                ('iddominio', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
                ('valor', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'r_dominio',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RIndexacion',
            fields=[
                ('idindexacion', models.IntegerField(serialize=False, primary_key=True)),
                ('cod_caja', models.IntegerField()),
                ('cod_carpeta', models.IntegerField()),
                ('folios', models.IntegerField()),
                ('num_radicado', models.IntegerField()),
                ('id_victima', models.CharField(max_length=45, null=True, blank=True)),
                ('nombre_victima', models.CharField(max_length=100, null=True, blank=True)),
                ('id_declara', models.CharField(max_length=45, null=True, blank=True)),
                ('nombre_declara', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'r_indexacion',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='RDomino',
        ),
        migrations.DeleteModel(
            name='RRegistro',
        ),
        migrations.DeleteModel(
            name='RRespons',
        ),
        migrations.DeleteModel(
            name='RResponssFuid',
        ),
    ]
