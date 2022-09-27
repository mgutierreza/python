import pyodbc as pyo
import pandas as pd
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoFilterType(nombreTabla):
    clase = ""
    cabeceraClase = generarCabeceraClase()
    claseEntity = generarClaseEntity(nombreTabla)
    nombreClase = generarNombreClase(nombreTabla)
    nombreArchivo = generarNombreArchivo(nombreClase)
    clase = cabeceraClase + claseEntity 
    
    #remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivo,'w')
    f.write(clase)
    f.close()

    return 

def generarClaseEntity(nombreTabla):
    claseEntity = ""
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Entities" + ENTER + "{" 
    pieClaseEntity = "}"

    cuerpoClaseEntity = generarCuerpoClaseEntity(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseEntity(nombreTabla):
    cuerpoClaseEntity = ""
    enumeradoItemType = ""
    enumeradoLstItemType = ""

    enumeradoItemType = enumeradoItemType + ENTER + TAB + "public enum " + nombreTabla + "FilterItemType : byte" + ENTER
    enumeradoItemType = enumeradoItemType + TAB + "{" + ENTER 
    enumeradoItemType = enumeradoItemType + 2*TAB + "Undefined," + ENTER
    enumeradoItemType = enumeradoItemType + 2*TAB + "ById," + ENTER
    enumeradoItemType = enumeradoItemType + TAB + "}" + 2*ENTER

    enumeradoLstItemType = enumeradoLstItemType + TAB + "public enum " + nombreTabla + "FilterLstItemType : byte" + ENTER
    enumeradoLstItemType = enumeradoLstItemType + TAB + "{" + ENTER 
    enumeradoLstItemType = enumeradoLstItemType + 2*TAB + "Undefined," + ENTER
    enumeradoLstItemType = enumeradoLstItemType + 2*TAB + "ById," + ENTER
    enumeradoLstItemType = enumeradoLstItemType + TAB + "}" + ENTER

    cuerpoClaseEntity = enumeradoItemType + enumeradoLstItemType 

    return cuerpoClaseEntity

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase = cabeceraClase +"using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return nombreTabla + 'FilterType'

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase