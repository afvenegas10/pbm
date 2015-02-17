# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from django.contrib import admin
from python_hol import views
from django.contrib.auth.decorators import login_required

admin.autodiscover()

handler400 = views.handler400
handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500
handler401 = views.handler401

urlpatterns = patterns('',
    #---home---
    url(r'^$', views.index, name='index'),
    url(r'^contacto/$', views.contacto, name='contacto'),
    url(r'^busqueda/$', views.busqueda_general, name='indexacion_listar'),
    url(r'^busqueda/fuid/$', views.busqueda_fuid, name='busqueda_fuid'),
    url(r'^busqueda/indexacion/$', views.busqueda_indexacion, name='busqueda_indexacion'),
    #---usuarios---
    url(r'^usuario/registrar/$', views.usuario_registrar, name='usuario_registrar'),
    url(r'^usuario/borrar/(?P<pk>\d+)/$', views.usuario_borrar, name='usuario_borrar'),
    url(r'^usuario/actualizar/(?P<pk>\d+)/$', views.usuario_actualizar, name='usuario_actualizar'), 
    url(r'^usuario/listar/$', views.usuario_listar, name='usuario_listar'),
    #---data---
    url(r'^migracion/excel/$', views.excel_migrar, name='migrar_excel/'),    
    #---fuid---
    url(r'^fuid/registrar/$', views.fuid_registrar, name='fuid_registrar'),
    url(r'^fuid/borrar/(?P<pk>\d+)/$', views.fuid_borrar, name='fuid_borrar'),
    url(r'^fuid/actualizar/(?P<pk>\d+)/$', views.fuid_actualizar, name='fuid_actualizar'),
    url(r'^fuid/listar/$', login_required(views.fuid_listar.as_view()), name='fuid_listar'),
    #---indexacion---
    url(r'^indexacion/registrar/$', views.indexacion_registrar, name='indexacion_registrar'),
    url(r'^indexacion/borrar/(?P<pk>\d+)/$', views.indexacion_borrar, name='indexacion_borrar'),
    url(r'^indexacion/actualizar/(?P<pk>\d+)/$', views.indexacion_actualizar, name='indexacion_actualizar'), 
    url(r'^indexacion/listar/$', login_required(views.indexacion_listar.as_view()), name='indexacion_listar'),
    url(r'^salir/$', views.usuarioCerrarSesion, name='usuario_salir'),
    
    url(r'^desargar/(?P<archivo>.*)/$', views.descargar_archivo, name='descargar_archivo'),
    #---admin---
    (r'^admin/', include(admin.site.urls)),
    url(r'^handler401/$', views.handler401, name='401'),
    #---rutas---
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'C:/Apache24/htdocs/mysite/src/python_hol/static'}),
    (r'^site_templates/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'C:/Apache24/htdocs/mysite/src/python_hol/templates'}),
)
