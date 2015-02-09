from python_hol.models import RFuid, RIndexacion, RDominio
from django.contrib import admin

class FuidAdmin(admin.ModelAdmin):
    list_display = ('num_orden', 'num_serie_sub_asuntos', 'fecha_extrema_inicio', 'fecha_extrema_fin', 'und_caja', 'und_carpeta', 'num_estante', 'num_entrepa_o', 'num_caja', 'soporte', 'frecuencia_consulta', 'notas')
    search_fields = ['num_orden', 'num_serie_sub_asuntos', 'und_caja', 'und_carpeta', 'num_estante', 'num_entrepa_o', 'num_caja', 'soporte', 'frecuencia_consulta', 'notas']
    list_filter = ['fecha_extrema_inicio', 'fecha_extrema_fin']
    
class IndexacionAdmin(admin.ModelAdmin):
    list_display = ('cod_caja', 'cod_carpeta', 'folios', 'num_radicado', 'id_victima', 'nombre_victima', 'id_declara', 'nombre_declara')
    search_fields = ['cod_caja', 'cod_carpeta', 'folios', 'num_radicado', 'id_victima', 'nombre_victima', 'id_declara', 'nombre_declara']
    
class DominioAdmin(admin.ModelAdmin):
    list_display = ('iddominio', 'nombre', 'valor')
    search_fields = ['iddominio', 'nombre', 'valor']    
        
#Register your models here.
admin.site.register(RFuid, FuidAdmin)
admin.site.register(RIndexacion, IndexacionAdmin)
admin.site.register(RDominio, DominioAdmin)