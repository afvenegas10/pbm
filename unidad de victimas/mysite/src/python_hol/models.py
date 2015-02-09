# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField?
    username = models.CharField(unique=True, max_length=30)    
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=0)
    is_staff = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField(default=datetime.now)
    
    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RDominio(models.Model):
    iddominio = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_dominio'



class RFuid(models.Model):
    num_orden = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    num_serie_sub_asuntos = models.CharField(max_length=100, blank=True, null=True)
    fecha_extrema_inicio = models.DateField(blank=True, null=True)
    fecha_extrema_fin = models.DateField(blank=True, null=True)
    und_caja = models.IntegerField(max_length=45, blank=True, null=True)
    und_carpeta = models.IntegerField(max_length=45, blank=True, null=True)
    und_tomo = models.CharField(max_length=45, blank=True, null=True)
    und_otro = models.CharField(max_length=45, blank=True, null=True)
    num_estante = models.IntegerField(blank=True, null=True)
    num_entrepa_o = models.IntegerField(db_column='num_entrepa\xf1o', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    num_caja = models.IntegerField(max_length=45, blank=True, null=True)
    num_folios = models.CharField(max_length=45, blank=True, null=True)
    soporte = models.CharField(max_length=45, blank=True, null=True)
    frecuencia_consulta = models.CharField(max_length=45, blank=True, null=True)
    notas = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_fuid'


class RIndexacion(models.Model):
    cod_carpeta = models.IntegerField(primary_key=True)
    cod_caja = models.IntegerField(max_length=45, blank=True, null=True)
    folios = models.IntegerField(max_length=45, blank=True, null=True)
    num_radicado = models.IntegerField(max_length=45, blank=True, null=True)
    id_victima = models.CharField(max_length=45, blank=True, null=True)
    nombre_victima = models.CharField(max_length=100, blank=True, null=True)
    id_declara = models.CharField(max_length=45, blank=True, null=True)
    nombre_declara = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_indexacion'
        
class Document(models.Model):
    filePath = models.CharField(max_length=500, blank=True, null=True)