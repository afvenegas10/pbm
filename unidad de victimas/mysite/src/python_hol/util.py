# -*- coding: utf-8 -*-
'''
Created on 18/11/2014

@author: afvenegas10
'''
from datetime import datetime
import datetime as dt

import xlrd

import sys
import time

from python_hol.models import RFuid, RIndexacion
from python_hol import log


#---procesos de registro---
def validaRegistro(registro):
    try:
        registroLen = len(registro)
        for a in range(0, registroLen):
            dato = registro[a]
            dato = str(dato).replace(" ", "")
            if dato == 'None' or dato == 'NOREGISTRA' or dato == None or dato == 'NOTIENE' or dato == 'FALTA' or dato == 'INDEX':
                registro[a] = ''
        return registro
    except Exception, e:
        log.error("error_Exception - validaRegistro: %s" % (e)) 


def listaExcel(rutaArchivo):
    try:
        try:
            workbook = abreLibro(rutaArchivo)
            if str(workbook).startswith("error_"):
                return workbook
            
            sheet = abreHoja(workbook)
            if str(sheet).startswith("error_"):
                return sheet
            
            ncols = sheet.ncols
            if not (ncols == 14 or ncols == 8):
                return "error_: No se esperaban "+str(ncols)+" columnas en el archivo."
            nrows = sheet.nrows
        except Exception, e:
            log.error("error_Exception - listaExcel.leeHoja: %s" % (e))
            return "error_: La lectura de la hoja fallo."
        
        tabla=[]
        errors=["error_: la validacion de campos a fallado, por tal razon no se a cargado ningun registro. Por favor tenga en cuenta las siguientes anotaciones he intente de nuevo"]
        #recorre filas
        for b in range(0, nrows):
        #define registro--------------------            
            #recorre columnas
            registro = []
            for c in range(0, ncols):
                #agrega registro
                try:
                    dato = sheet.cell_value(b,c)
                except Exception, e:
                    log.error("error_Exception - listaExcel.leeCelda: %s" % (e))
                    errors.append(['error_: fila ' + str(b), 'La lectura de la cadena "'+str(dato)+'" columna:' + str(c) + " fallo."])                        
                if isinstance(dato, basestring):                
                    try:
                        #codifica las cadenas para mostrar Ã±
                        dato = dato.encode("utf-8")            
                    except Exception, e:
                        log.error("error_Exception - listaExcel.encodeCelda : %s" % (e))
                        errors.append(['error_: fila ' + str(b), 'La decodificacion del campo "'+str(dato)+'" columna:' + str(c) + " fallo."])
                else:
                    try:
                        #convierte en enteros los numeros
                        dato = int(float(str(dato)))
                        if (c == 3 or c == 4) and ncols==14:
                            try:
                                #trata de leer el campo como fecha
                                dato = xlrd.xldate_as_tuple(dato, workbook.datemode)
                                dato = str(dt.datetime(*dato[:3]))
                                dato = datetime.strptime(dato,"%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d")
                            except Exception, e:
                                log.error("error_Exception.date: %s" % (e))
                                errors.append(['error_: fila ' + str(b), 'La lectura del numero "'+str(dato)+'" columna:' + str(c) + " fallo, no pudo ser leido como fecha."])
                    except Exception, e:
                        log.error("error_Exception - listaExcel.int : %s" % (e))
                        errors.append(['error_: fila ' + str(b), 'La lectura del numero "'+str(dato)+'" columna:' + str(c) + " fallo, no pudo ser leido como numero."])  
                #log.info("dato:" + dato)  
                registro.insert(ncols, dato)
            #log.info("registro:" + str(registro))
            #valida los registros para identificar fallos en la informacion
            if b > 0:
                if ncols == 14:
                    registro = validaRegistro(registro)
                    message = validaFuid(registro, b)
                    if not str(message).startswith("ok_"):
                        errors.append(message)
                elif ncols == 8:
                    registro = validaRegistro(registro)
                    message = validaIndexacion(registro, b)
                    if not str(message).startswith("ok_"):
                        errors.append(message)
            else:            
                try:
                    if ncols == 14 and not (
                                            "NUMERO DE ORDEN" == registro[0] and
                                            "CODIGO" == registro[1] and      
                                            "NOMBRE DE LAS SERIES, SUBSERIES DOCUMENTALES" == registro[2] and
                                            "Inicial" == registro[3] and
                                            "Final" == registro[4] and
                                            "Caja" == registro[5] and
                                            "Carpeta" == registro[6] and       
                                            "Tomo" == registro[7] and
                                            "Otro" == registro[8] and
                                            "N° FOLIOS" == registro[9] and
                                            "N° CAJA" == registro[10] and
                                            "SOPORTE" == registro[11] and
                                            "FRECUENCIA DE CONSULTA" == registro[12] and
                                            "NOTAS" == registro[13]
                                            ):                    
                        return "error_: se identifica como INVENTARIO DOCUMENTAL - FORMATO, pero no cumple con el formato, porfavor revise los titulos de columna he intente de nuevo."
                    elif ncols == 8 and not (
                        "CODIGO CAJA" == registro[0] and
                        "CODIGO CARPETA" == registro[1] and      
                        "FOLIOS" == registro[2] and
                        "NUMERO RADICADO" == registro[3] and
                        "IDENTIFICACION VICTIMA" == registro[4] and
                        "NOMBRE VICTIMA" == registro[5] and
                        "IDENTIFICACION DECLARANTE" == registro[6] and       
                        "NOMBRE DECLARANTE" == registro[7]
                        ):                     
                        return "error_: se identifica como INDEXACIÓN DIGITALIZACIÓN - FORMATO, pero no cumple con el formato, porfavor revise los titulos de columna he intente de nuevo."
                except Exception, e:
                    log.error("error_Exception - listaExcel.validaFormato: %s" % (e)) 
                                                 
            tabla.append(registro)
        
        #log.info(str(errors)) 
        HtmlTabla = htmlTabla(tabla)
        if len(errors) > 1:
            HtmlTabla = "error_" +  str(HtmlTabla) + "<br>" + str(htmlErrorsMensaje(errors))
            
        return HtmlTabla
    except Exception, e:
        log.error("error_Exception - listaExcel: %s" % (e))
    

def cargaExcel(rutaArchivo):
    try:
        log.info("cargaExcelInicio"+str(datetime.now()))
        errors=["error_: La carga de los siguientes resgistros fallo, los demas fueron cargados exitosamente: "]
        
        try:
            workbook = abreLibro(rutaArchivo)
            if str(workbook).startswith("error_"):
                return workbook
            
            sheet = abreHoja(workbook)
            if str(sheet).startswith("error_"):
                return sheet
            
            ncols = sheet.ncols
            if not (ncols == 14 or ncols == 8):
                return "error_: No se esperaban "+str(ncols)+" columnas en el archivo."
            nrows = sheet.nrows
        except Exception, e:
            log.error("error_Exception - cargaExcel.leeHoja: %s" % (e))
            return "error_: La lectura de la hoja fallo."
                
        for b in range(1, nrows):
            registro = []
            for c in range(0, ncols):
                #agrega registro
                try:
                    dato = sheet.cell_value(b,c)
                except Exception, e:
                    log.error("error_Exception - cargaExcel.leeCelda : %s" % (e))
                    errors.append(['error_: fila ' + str(b), 'La lectura de la cadena "'+str(dato)+'" columna:' + str(c) + " fallo."])                        
                if isinstance(dato, basestring):                
                    try:
                        #codifica las cadenas para mostrar Ã±
                        dato = dato.encode("utf-8")            
                    except Exception, e:
                        log.error("error_Exception - cargaExcel.encode: %s" % (e))
                        errors.append(['error_: fila ' + str(b), 'La decodificacion del campo "'+str(dato)+'" columna:' + str(c) + " fallo."])
                else:
                    try:
                        #convierte en enteros los numeros
                        dato = int(float(str(dato)))
                        if (c == 3 or c == 4) and ncols==14:
                            try:
                                #trata de leer el campo como fecha                   
                                dato = xlrd.xldate_as_tuple(dato, workbook.datemode)
                                dato = str(dt.datetime(*dato[:3]))
                                dato = datetime.strptime(dato,"%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d")
                            except Exception, e:
                                log.error("error_Exception - cargaExcel.date: %s" % (e))
                                errors.append(['error_: fila ' + str(b), 'La lectura del numero "'+str(dato)+'" columna:' + str(c) + " fallo, no pudo ser leido como fecha."])
                    except Exception, e:
                        log.error("error_Exception - cargaExcel.int: %s" % (e))
                        errors.append(['error_: fila ' + str(b), 'La lectura del numero "'+str(dato)+'" columna:' + str(c) + " fallo, no pudo ser leido como numero."])  
                #log.info("dato:" + dato)  
                registro.insert(ncols, dato)
            #log.info("registro:" + str(registro))
            #valida los registros para identificar fallos en la informacion
            try:
                if ncols == 14:
                    message = insertaFuid(registro, b)
                    if not str(message).startswith("ok_"):
                        message = message[8:len(message)]
                        if str(message).startswith("1062"):
                            errors.append("El registro: " + str(b) + " ya existe.")
                        elif str(message).startswith("1300"):
                            errors.append("El registro: " + str(b) + " no es valido.")
                        else:
                            log.info(str(message)) 
                            errors.append("El registro: " + str(b) + " no se cargó.")
                    else:
                        message = "ok_carga de registros FUID"                    
                elif ncols == 8:
                    message = insertaIndexacion(registro, b)
                    if not str(message).startswith("ok_"):
                        print "message: [" + str(message) + "]"
                        message = message[8:len(message)]
                        print "error_message: [" + str(message) + "]"
                        if str(message).startswith("1062"):
                            errors.append("El registro: " + str(b) + " ya existe.")
                        elif str(message).startswith("1300"):
                            errors.append("El registro: " + str(b) + " no es valido.")
                        else:
                            errors.append("El registro: " + str(b) + " no se cargó.")
                    else:
                        message = "ok_carga de registros de indexacion"
            except Exception, e:
                log.error("error_Exception - cargaExcel.carga: %s" % (e)) 
        if len(errors) > 1:
            message = "error_"+str(htmlErrorMensaje(errors))
        
        log.info("cargaExcelFin"+str(datetime.now())) 
        return message
    except Exception, e:
        log.error("error_Exception - cargaExcel: %s" % (e))


def validaIndexacion(registro, index):
        try:
            error=['error_: fila ' + str(index)]   
                 
            Cod_caja = registro[0]
            Cod_carpeta = registro[1]        
            Folios = registro[2]
            Num_radicado = registro[3]
            Id_victima = registro[4]
            Nombre_victima = registro[5]
            Id_declara = registro[6]
            Nombre_declara = registro[7]            
            
            if not esNumero(Cod_caja):
                    error.append(campoNoNumerico('"codigo de caja"',Cod_caja)) 
            
            if Cod_carpeta == "":
                error.append(campoNone('"codigo carpeta"'))  
            elif not esNumero(Cod_carpeta):
                error.append(campoNoNumerico('"codigo de carpeta"',Cod_carpeta))
                          
            if not esNumero(Folios):
                error.append(campoNoNumerico('"numero de folio"', Folios))               
            if not esNumero(Num_radicado):
                error.append(campoNoNumerico('"numero de radicado"', Num_radicado))        
            if not esNumero(Id_victima):
                error.append(campoNoNumerico('"identificacion de victima"', Id_victima))        
            if not esNumero(Id_declara):
                error.append(campoNoNumerico('"identificacion de declarante"', Id_declara))
            
            if not esAlfabetico(Nombre_victima):
                error.append(campoNoAlfabetico('"nombre de la victima"', Nombre_victima))            
            if not esAlfabetico(Nombre_declara):     
                error.append(campoNoAlfabetico('"nombre del declarante"', Nombre_declara))
    
            if len(error) == 1:
                return "ok_Indexacion valido."
            else:
                return error
        except Exception, e:
            log.error("error_Exception - validaIndexacion: %s" % (e)) 

     
def validaFuid(registro, index):
    try:
        error=['error_: fila ' + str(index)]
        
        Num_orden = registro[0]
        Codigo = registro[1]            
        Num_serie_sub_asuntos = registro[2]    
        Fecha_extrema_inicio = registro[3]
        Fecha_extrema_fin = registro[4]
        Und_caja = registro[5]
        Und_carpeta = registro[6]
        Und_tomo = registro[7]
        Und_otro = registro[8]
        Num_folios = registro[9]
        Num_caja = registro[10]
        Soporte = registro[11]
        Frecuencia_consulta = registro[12]
        Notas = registro[13]
                        
        if Num_orden == "":
                error.append(campoNone('"numero de orden"'))
        elif not esNumero(Num_orden):            
            error.append(campoNoNumerico('"numero de orden"',Num_orden))
            
        if not esNumero(Codigo):            
            error.append(campoNoNumerico('"codigo"', Codigo))
        if not  esNumero(Und_tomo):            
            error.append(campoNoNumerico('"numero de tomo de la unidad"', Und_tomo))
        if not esNumero(Und_otro):            
            error.append(campoNoNumerico('"numero de otro de la unidada"', Und_otro))
        if not esNumero(Num_folios):            
            error.append(campoNoNumerico('"numero de folio de la unidada"', Num_folios))
        if not esNumero(Und_caja):            
            error.append(campoNoNumerico('"numero de caja de la unidada"',Und_caja))
        if not esNumero(Und_carpeta):         
            error.append(campoNoNumerico('"numero de carpeta de la unidada"',Und_carpeta))
        if not esNumero(Num_caja):         
            error.append(campoNoNumerico('"numero de caja"',Num_caja))
        
        if not esAlfabetico(Num_serie_sub_asuntos):     
            error.append(campoNoAlfabetico('"numero de serie, subserie, asuntos"', Num_serie_sub_asuntos))      
        if not esAlfabetico(Soporte):     
            error.append(campoNoAlfabetico('"soporte"', Soporte))            
        if  not esAlfabetico(Frecuencia_consulta):          
            error.append(campoNoAlfabetico('"frecuencia de consulta"',Frecuencia_consulta))  
        
        if not esFecha(Fecha_extrema_inicio):
            error.append(campoNoFecha('"fecha extrema inicio"', Fecha_extrema_inicio))        
        if not esFecha(Fecha_extrema_fin):
            error.append(campoNoFecha('"fecha extrema fin"', Fecha_extrema_fin))
            
        if not esNota(Notas): 
            error.append(campoNoNota('"notas"', Notas))      
        
        if len(error) == 1:
            return "ok_FUID valido."
        else:
            return error
    except Exception, e:
        log.error("error_Exception - validaFuid: %s" % (e))
        

def insertaIndexacion(registro, index):

    try:
        registro=validaRegistro(registro)
    
        Cod_caja = registro[0]
        Cod_carpeta = registro[1]
        Folios = registro[2]
        Num_radicado = registro[3]
        Id_victima = registro[4]
        Nombre_victima = registro[5]
        Id_declara = registro[6]
        Nombre_declara = registro[7]
        
        cadena = 'Cod_caja: '+ str(Cod_caja) + ' Cod_carpeta: '+ str(Cod_carpeta) + ' Folios: '+ str(Folios) + ' Num_radicado: '+ str(Num_radicado) + ' Id_victima: '+ str(Id_victima) + ' Nombre_victima: '+ str(Nombre_victima) + ' Id_declara: '+ str(Id_declara) + ' Nombre_declara: '+ str(Nombre_declara)
        
        message = validaIndexacion(registro, index)
        if not str(message).startswith("ok_"):
            #log.info('validaIndexacion (no es valido) '+str(index)+' - '+ cadena)
            return 'error_: 1300 validaIndexacion (no es valido) '+str(index)+' - '+ cadena
        
        if Cod_caja == "":
            Cod_caja = None
        if Cod_carpeta == "":
            Cod_carpeta = None
        if Folios == "":
            Folios = None
        if Num_radicado == "":
            Num_radicado = None
        if Id_victima == "":
            Id_victima = None
        if Id_declara == "":
            Id_declara = None
        
        """
        log.info('insertaIndexacion - '+ cadena )
        """
        
        try:
            RIndexacion.objects.create(
                                        cod_caja =  Cod_caja,
                                        cod_carpeta  =  Cod_carpeta,
                                        folios = Folios,
                                        num_radicado = Num_radicado,
                                        id_victima = Id_victima,
                                        nombre_victima = Nombre_victima,
                                        id_declara = Id_declara,
                                        nombre_declara = Nombre_declara
                                        )
        except Exception, e:
            log.error("error_Exception - insertaIndexacion.insert: %s" % (e))
            message = 'error_: '
            if str(e[0])== "1062":
                message = message + '1062'
            return message
        
        return 'ok_registrar indexacion'
    except Exception, e:
        log.error("error_Exception - insertaIndexacion: %s" % (e))

def insertaFuid(registro, index):
    
    try:
        registro=validaRegistro(registro)
        
        Num_orden = registro[0]
        Codigo = registro[1]            
        Num_serie_sub_asuntos = registro[2]    
        Fecha_extrema_inicio = registro[3]
        Fecha_extrema_fin = registro[4]
        Und_caja = registro[5]
        Und_carpeta = registro[6]
        Und_tomo = registro[7]
        Und_otro = registro[8]
        Num_folios = registro[9]
        Num_caja = registro[10]
        Soporte = registro[11]
        Frecuencia_consulta = registro[12]
        Notas = registro[13]
        
        cadena = 'num_orden: '+ str(Num_orden) + ' codigo:'+ str(Codigo) +  ' num_serie_sub_asuntos:'+ str(Num_serie_sub_asuntos) +  ' fecha_extrema_inicio:'+ str(Fecha_extrema_inicio) + ' fecha_extrema_fin:'+ str(Fecha_extrema_fin) +  ' und_caja:' + str(Und_caja) + ' und_carpeta:' + str(Und_carpeta) +   ' und_tomo:'+ str(Und_tomo) +  ' und_otro:'+ str(Und_otro) +  ' num_caja:' + str(Num_caja) +   ' soporte:' + str(Soporte) + ' frecuencia_consulta:' + str(Frecuencia_consulta) + ' notas:' + str(Notas)
    
        message = validaFuid(registro, index)
        if not str(message).startswith("ok_"):
            return 'error_: 1300 validaRegistro (no es valido) '+str(index)+' - '+ cadena
    
        """
        log.info('inserataFuid - '+ cadena )
        """
        
        if Num_serie_sub_asuntos == "":
            Num_serie_sub_asuntos = None
        if Num_orden == "":
            Num_orden = None
        if Codigo == "":
            Codigo = None
        if Und_caja == "":
            Und_caja = None    
        if Und_carpeta == "":
            Und_carpeta = None    
        if Und_tomo == "":
            Und_tomo = None    
        if Und_otro == "":
            Und_otro = None    
        if Num_folios == "":
            Num_folios = None    
        if Num_caja == "":
            Num_caja = None
        
        if Fecha_extrema_inicio == "":        
            Fecha_extrema_inicio = None    
        else:
            try:            
                Fecha_extrema_inicio = datetime.strptime(Fecha_extrema_inicio,"%Y/%m/%d").strftime("%Y-%m-%d")
            except Exception, e:
                log.error("error_Exception - insertaFuid.formatInicio: %s" % (e))
                return 'error_: insertaFuid'+str(index)+' (no se pudo dar formato a la fecha inicio) - '+ cadena
                
        if Fecha_extrema_fin == "":
            Fecha_extrema_fin = None
        else:
            try:
                Fecha_extrema_fin = datetime.strptime(Fecha_extrema_fin,"%Y/%m/%d").strftime("%Y-%m-%d")
            except Exception, e:
                log.error("error_Exception - insertaFuid.formatFin: %s" % (e))
                return 'error_: insertaFuid'+str(index)+' (no se pudo dar formato a la fecha fin) - '+ cadena
            
        try:                                
            RFuid.objects.create(
                                 num_orden=Num_orden,
                                 codigo=Codigo,
                                 num_serie_sub_asuntos=Num_serie_sub_asuntos,
                                 fecha_extrema_inicio=Fecha_extrema_inicio,
                                 fecha_extrema_fin=Fecha_extrema_fin,
                                 und_caja=Und_caja,
                                 und_carpeta=Und_carpeta,
                                 und_tomo=Und_tomo,
                                 und_otro=Und_otro,
                                 num_caja=Num_caja,
                                 num_folios=Num_folios,
                                 soporte=Soporte,
                                 frecuencia_consulta=Frecuencia_consulta,
                                 notas=Notas
                                )
        except Exception, e:
            log.error("error_Exception - insertaFuid.insert: %s" % (e))
            message = 'error_: '
            if e[0]== "1062":
                message = message + ' %s' % (e[0])        
            return message
            
        return 'ok_registrar Fuid'+str(index)+' - '+ cadena
    except Exception, e:
        log.error("error_Exception - insertaIndexacion: %s" % (e))
        
        
def htmlErrorsMensaje(msj):
    try:
        msjLen = len(msj)
        error = '<div id="error_message">'+str(msj[0]) + '<br><br><ul">'
        for a in range(1, msjLen):
            errorSub = msj[a]
            error = error+"<li>" + str(errorSub[0]) + '<ul">'
            errorSubLen = len(errorSub)    
            for b in range(1, errorSubLen):
                error = error + "<br>    - " + str(errorSub[b])
            error = error + "</ul>"
        error = error + "</li>"
        return error+"</ul></div>"
    except Exception, e:
        log.error("error_Exception - htmlErrorsMensaje: %s" % (e))

def htmlErrorMensaje(msj):
    try:        
        msjLen = len(msj)
        error = '<div id="error_message">'+str(msj[0]) + '<br><br><ul">'
        for a in range(1, msjLen):
            errorSub = msj[a]
            error = error+"<li>" + str(errorSub) + "</li>"
        msj = error+"</ul></div>"
        return msj
    except Exception, e:
        log.error("error_Exception - htmlErrorMensaje: %s" % (e))


def htmlTabla(tabla):
    try:
        htmlTabla = '<table id="lista_tabla">'
        #---arma encabezado---
        try:        
            encabezado = tabla[0]
            lenEncabezado = len(encabezado)
        except Exception, e:
            log.error("error_Exception - htmlTabla.encabezado: %s" % (e))
            return 'error_: La carga del encabezado del archivo fallo. posiblemente se deba a un registro vacio'

        htmlTabla =  htmlTabla + '<tr><th>#</th>'
        for a in range(0, lenEncabezado):
            dato = encabezado[a]
            htmlTabla =   htmlTabla + '<th>' + dato + '</th>'
        htmlTabla =  htmlTabla + '</tr>'
        #---arma contenido---
        lenTabla = len(tabla)
        for a in range(1, lenTabla):
            registro = tabla[a]
            lenRegistro = len(registro)
            htmlTabla =  htmlTabla + '<tr><td>'+str(a)+'.</td>'
            for c in range(0, lenRegistro):
                dato = registro[c]
                #if isinstance(dato, basestring):
                htmlTabla =   htmlTabla + '<td>' + str(dato) + '</td>'
            htmlTabla =  htmlTabla + '</tr>'
        htmlTabla =  htmlTabla + '</table>'
        return htmlTabla
    except Exception, e:
        log.error("error_Exception - htmlTabla: %s" % (e))


def abreHoja(workbook):
    try:
        try:
            sheet = workbook.sheet_by_index(0)
        except IndexError, e:
            log.info("error_IndexError - abreHoja.index: %s" % (e))
            return "error_: El archivo no tiene hojas para leer."
        except Exception, e:
            log.error("error_Exception - abreHoja.sheet: %s" % (e))
            return 'error_: La lectura de la hoja fallo.'    
        return sheet
    except Exception, e:
        log.error("error_Exception - abreHoja: %s" % (e))


def abreLibro(rutaArchivo):
    try:
        if not rutaArchivo.endswith(".xlsx"):
            return "error_: El archivo no tiene la extencion esperada, o la ruta no es es interpretable (c:/ruta/archivo.xlsx)"
        if rutaArchivo == None:
            return "error_: Es necesario que ingrese una ruta valida."
        
        try:
            workbook = xlrd.open_workbook(rutaArchivo)
        except IOError, (errno, strerror):
            log.error("error_IOError: (%s): %s" % (errno, strerror))
            return "error_: El archivo no fue encontrado."
        except Exception as e:
            log.error("error_Exception - abreLibro: %s" % (e))
            return "error_: A ocurrido un fallo al intentar cargar el archivo, posiblemente se deba a un formato incompatible o un archivo dañado"
    
        return workbook
    except Exception, e:
        log.error("error_Exception - abreLibro: %s" % (e))


#---mesnajes de error---
def campoNone(msg):
    return("El campo " + str(msg) + ", no puede ser vacio.")

def campoNoNumerico(msg, numero):
    return("El campo " + str(msg) + ':"'+str(numero)+'", debe ser numerico.')

def campoNoAlfabetico(msg, campo):
    return("El campo " + str(msg) + ':"'+str(campo)+'", debe ser alfabetico.')

def campoNoFecha(msg, fecha):
    return('El campo ' + str(msg) + ':"'+str(fecha)+'", no es una fecha valida ("AAAA/MM/DD").')

def campoNoNota(msg, Notas):
    return('El campo ' + str(msg)+ ':"' + str(Notas) +  '", no es una nota valida (123 o 123/456/...).')

#---validaciones de cadenas---
def esFecha(fecha):
    try:
        if fecha == "":
            return True
        fecha =  datetime.strptime(str(fecha), "%Y/%m/%d")
        return True
    except Exception:       
        return False


def esNota(notas):
    notas = str(str(notas).replace(" ", ""))
    notas = notas.replace("/", "")
    try:
        if notas == "":
            return True
        return notas.isdigit()
    except Exception:
        return False
    return False


def esNumero(numero):
    numero = str(str(numero).replace(" ", ""))
    try:
        if numero == "":
            return True
        return numero.isdigit()
    except Exception:
        return False
    return False


def esAlfabetico(cadena):
    try:
        cadena = str(cadena)
        cadena = cadena.replace(" ", "")
        cadena = cadena.replace("Ñ", "")
        cadena = cadena.replace("Á", "")
        cadena = cadena.replace("É", "")
        cadena = cadena.replace("Í", "")
        cadena = cadena.replace("Ó", "")
        cadena = cadena.replace("Ú", "")
        if cadena == '':
            return True
        message = cadena.isalpha()
    except Exception:
        message = False
    return message
