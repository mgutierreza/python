import pyodbc as pyo
import pandas as pd
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoException(nombreTabla):
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
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Exceptions" + ENTER + "{" 
    pieClaseEntity = "}"

    cuerpoClaseEntity = generarCuerpoClaseEntity(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseEntity(nombreTabla):
    cuerpoClaseEntity = ""

    cuerpoClaseEntity = cuerpoClaseEntity + ENTER + TAB + "public class " + nombreTabla + "Exception : CustomException" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + TAB + "{" + ENTER 
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "public override string CustomMessage" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "{" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "get" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "{" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 4*TAB + "return \"Prueba Fail inserting header\";" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "}" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "}" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + TAB + "}" + ENTER

    return cuerpoClaseEntity

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase = cabeceraClase +"using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return nombreTabla + 'Exception'

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase