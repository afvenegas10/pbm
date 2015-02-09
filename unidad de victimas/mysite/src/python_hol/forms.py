# -*- coding: utf-8 -*-
from django import forms
from python_hol.models import AuthUser, RFuid, RIndexacion
from django.forms.widgets import PasswordInput
from django.forms.extras.widgets import SelectDateWidget

campoVacio = {'required': 'Debe diligenciar el campo.'}
campoUnico = {'required': 'Debe diligenciar el campo.','unique': 'El registro ya existe, con esta informacion.','max_value': 'Asegúrese de este valor es menor que o igual a 2147483647.', 'invalid': 'Debe corregir el valor.'}
fechaInvalida = {'invalid': 'Debe corregir el valor.'}
campoInvalido = {'invalid': 'Debe corregir el valor.'}


class usuarioForm(forms.ModelForm):
    #id = forms.CharField(label='Id', max_length=11)
    password = forms.CharField(label="Constraseña",  help_text="Constraseña",max_length=30, widget=PasswordInput(), error_messages=campoVacio)
    #last_login = forms.DateTimeField(label='Ultimo ingreso')
    #is_superuser = forms.BooleanField(label='Super usuario')
    username = forms.CharField(label="Nombre de usuario",  help_text="Nombre de usuario",max_length=30, error_messages=campoUnico)
    first_name = forms.CharField(label="Nombre",  help_text="Nombre",required=False,max_length=30)
    last_name = forms.CharField(label="Apellido",  help_text="Apellido",required=False,max_length=30)
    #email = forms.EmailField(label="Correo electronico",  help_text="Correo electronico",required=False,max_length=254)
    #is_staff = forms.BooleanField(label='is_staff')
    #is_active = forms.BooleanField(label='Activo')
    #date_joined = forms.CharField(label='Fecha registro', max_length=6)
    
    class Meta:
        model = AuthUser
        fields = ('username','password','first_name','last_name')

        
class fuidForm(forms.ModelForm):

    #Soporte = RDominio.objects.all().filter(nombre='soporte').values_list('iddominio','valor')
    #Frecuencia_consulta = RDominio.objects.all().filter(nombre='frecuencia_consulta').values_list('iddominio','valor')
    Soporte = (
                ('', ''),
                ('PAPEL', 'PAPEL'),
                ('DIGITAL', 'DIGITAL'),
    )
    Frecuencia_consulta = (
                ('', ''),
                ('MEDIA', 'MEDIA'),
                ('ALTA', 'ALTA'),
                ('BAJA', 'BAJA'),
    )
    #idregistro = forms.CharField(max_length=45, required=False)
    num_orden = forms.IntegerField(label="Numero de orden", help_text="Numero de orden", min_value=0, error_messages=campoUnico,required=False)
    codigo = forms.IntegerField(label='Codigo',help_text="codigo", min_value=0, error_messages=campoUnico,required=False)
    num_serie_sub_asuntos = forms.CharField(label="Numero de serie, subserie, asunto", required=False,  help_text="Numero de serie, subserie, asunto.", error_messages= campoInvalido)
    fecha_extrema_inicio = forms.DateField(label='Fecha extrema inicial', required=False, error_messages=fechaInvalida, help_text="feha extrema inicial ej: YYYY/MM/DD.", input_formats=['%Y/%m/%d'],)
    fecha_extrema_fin = forms.DateField(label='Fecha extrema final', required=False, error_messages=fechaInvalida, help_text="feha extrema final ej: YYYY/MM/DD.", input_formats=['%Y/%m/%d'],)
    und_caja = forms.IntegerField(label="Codigo de caja",  required=False, help_text="codigo de caja de la unidad de conservacion.", min_value=0, error_messages=campoInvalido)
    und_carpeta = forms.IntegerField(label="Codigo de carpeta",  required=False, help_text="codigo de carpeta de la unidad de conservacion.", min_value=0, error_messages=campoInvalido)
    und_tomo = forms.IntegerField(label="Codigo de tomo",  help_text="codigo de tomo.", required=False, min_value=0, error_messages=campoInvalido)
    und_otro = forms.IntegerField(label="Codigo de otro",  help_text="codigo de otro.", required=False, min_value=0, error_messages=campoInvalido)
    #num_estante = forms.CharField(max_length=45, max_length=45, blank=True, null=True)
    #num_entrepa_o = forms.CharField(max_length=45, max_length=45, blank=True, null=True)
    num_folios = forms.IntegerField(label="Numero de folio",  help_text="Numero de folio.", required=False, min_value=0)
    num_caja = forms.IntegerField(label="Numero de caja",  required=False, help_text="Numero de caja", min_value=0, error_messages=campoInvalido)    
    soporte = forms.ChoiceField(label="Soporte",  help_text="soporte", required=False, choices=Soporte)
    frecuencia_consulta = forms.ChoiceField(label="Frecuencia de consulta",  help_text="frecuencia de consulta", required=False, choices=Frecuencia_consulta)
    notas = forms.CharField(label="Notas",  required=False, help_text="numero de radicados ej: 123 ó 123/456/...", max_length=100, error_messages=campoVacio)
    

                
    class Meta:
        model = RFuid
        fieldsets=[
                    ('Dateinformation',{'fields':['codigo']}),
        ]  
        fields = (                    
                    'num_orden',
                    'codigo',                                      
                    'num_serie_sub_asuntos', 
                    'fecha_extrema_inicio', 
                    'fecha_extrema_fin', 
                    'und_caja', 
                    'und_carpeta',
                    'und_tomo',
                    'und_otro',
                    'num_folios',
                    'num_caja', 
                    'soporte', 
                    'frecuencia_consulta', 
                    'notas'
                  )        
            



class indexacionForm(forms.ModelForm):    
    cod_carpeta=forms.IntegerField(label="Codigo de carpeta",  help_text="Codigo de carpeta",min_value=0, error_messages=campoUnico,required=False)
    cod_caja=forms.IntegerField(label="Codigo de caja",  help_text="Codigo de caja", min_value=0, required=False, error_messages=campoInvalido)
    folios=forms.IntegerField(label="Numero de folio",  help_text="Numero de folio",min_value=0, required=False, error_messages=campoInvalido)
    num_radicado=forms.IntegerField(label="Numero de radicado",  help_text="Numero de radicado",min_value=0, required=False, error_messages=campoInvalido)
    id_victima=forms.IntegerField(label="Identificacion de victima",  help_text="Identificacion de victima",min_value=0, required=False, error_messages=campoInvalido)
    nombre_victima=forms.CharField(label="Nombre de victima",  help_text="Nombre de victima",max_length=100, required=False)
    id_declara=forms.IntegerField(label="Identificacion de declarante",  help_text="Identificacion de declarante",min_value=0, required=False, error_messages=campoInvalido)
    nombre_declara=forms.CharField(label="Nombre de declarante",  help_text="Nombre de declarante",max_length=100, required=False)

    class Meta:
        model = RIndexacion
        fields = ('cod_carpeta', 'cod_caja', 'folios', 'num_radicado', 'id_victima', 'nombre_victima', 'id_declara', 'nombre_declara')


class documentoForm(forms.Form):
    filePath = forms.CharField(label='ruta', required=False)


class busquedaForm(forms.Form):
    buscar = forms.CharField(label='buscar', required=False)

    
class usuarioAutenticacionForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=128, widget=PasswordInput())