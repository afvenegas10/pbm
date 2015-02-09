# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=160, unique=True, null=True, blank=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=510, null=True, blank=True)),
                ('codename', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=256, null=True, blank=True)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=60, unique=True, null=True, blank=True)),
                ('first_name', models.CharField(max_length=60, null=True, blank=True)),
                ('last_name', models.CharField(max_length=60, null=True, blank=True)),
                ('email', models.CharField(max_length=508, null=True, blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=400, null=True, blank=True)),
                ('action_flag', models.IntegerField()),
                ('change_message', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('app_label', models.CharField(max_length=200, null=True, blank=True)),
                ('model', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('app', models.CharField(max_length=510, null=True, blank=True)),
                ('name', models.CharField(max_length=510, null=True, blank=True)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=80, serialize=False, primary_key=True)),
                ('session_data', models.TextField(null=True, blank=True)),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RDomino',
            fields=[
                ('iddomino', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
                ('valor', models.CharField(max_length=45, null=True, blank=True)),
                ('padre', models.CharField(max_length=45, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'r_domino',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RFuid',
            fields=[
                ('idfuid', models.IntegerField(serialize=False, primary_key=True)),
                ('entidad_remitente', models.CharField(max_length=45, null=True, blank=True)),
                ('entidad_productora', models.CharField(max_length=45, null=True, blank=True)),
                ('unidad_administrativa', models.CharField(max_length=45, null=True, blank=True)),
                ('oficina_productora', models.CharField(max_length=45, null=True, blank=True)),
                ('objeto', models.CharField(max_length=45, null=True, blank=True)),
                ('num_hoja', models.IntegerField(null=True, blank=True)),
                ('total_hojas', models.IntegerField(null=True, blank=True)),
                ('registro_entrada', models.CharField(max_length=45, null=True, blank=True)),
                ('numero_transferencia', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'r_fuid',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RRegistro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idregistro', models.IntegerField()),
                ('numero_orden', models.IntegerField(null=True, blank=True)),
                ('codigo', models.CharField(max_length=45, null=True, blank=True)),
                ('num_serie_sub_asuntos', models.IntegerField(null=True, blank=True)),
                ('fecha_extrema_inicio', models.CharField(max_length=45, null=True, blank=True)),
                ('fecha_extrema_fin', models.CharField(max_length=45, null=True, blank=True)),
                ('unid_conservacion', models.IntegerField(null=True, blank=True)),
                ('num_folios', models.CharField(max_length=45, null=True, blank=True)),
                ('soporte', models.CharField(max_length=100, null=True, blank=True)),
                ('frecuencia_consulta', models.CharField(max_length=45, null=True, blank=True)),
                ('notas', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'r_registro',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RRespons',
            fields=[
                ('idrespons', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre1', models.CharField(max_length=45, null=True, blank=True)),
                ('nombre2', models.CharField(max_length=45, null=True, blank=True)),
                ('apellido1', models.CharField(max_length=45, null=True, blank=True)),
                ('apellido2', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'r_respons',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RResponssFuid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cargo', models.CharField(max_length=45, null=True, blank=True)),
                ('firma', models.CharField(max_length=45, null=True, blank=True)),
                ('lugar', models.CharField(max_length=45, null=True, blank=True)),
                ('fecha', models.DateField(null=True, blank=True)),
                ('rol', models.IntegerField()),
            ],
            options={
                'db_table': 'r_responss_fuid',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
