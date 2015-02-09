    
<input type="file" name="filePath"  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" >

def data_cargar_excel(request):
    return render_to_response('data/data_cargar_excel.html')
    
def data_listar_excel(request):
    return HttpResponse('hola')
2590292
#---timestamp---
import time
print str(datetime.now())

#---choise--
Soporte= (('PAPEL'))
first_name=forms.ChoiceField(label='nombre', choices=Soporte)
    
date_joined = models.DateTimeField(default=datetime.now)

#---formato de fechas---
buscar = datetime.strptime(buscar,"%Y-%m-%d").strftime("%Y, %m, %d")

#---css fieldset---
fieldset{
    border-radius:10px;
    width: 35%;
}
                  