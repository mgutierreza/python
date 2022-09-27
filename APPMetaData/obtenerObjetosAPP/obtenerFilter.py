import pyodbc as pyo
import pandas as pd
from consultaDatos import obtenerMetaDataClavePrincipal
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoFilter(nombreTabla):
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
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Entities" + ENTER + "{" + ENTER
    cabeceraClaseEntity = cabeceraClaseEntity + TAB + "public class " + generarNombreClase(nombreTabla) + ENTER + TAB + "{" 
    pieClaseEntity = TAB + "}" + ENTER + "}" + ENTER

    cuerpoClaseEntity = generarCuerpoClaseEntity(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseEntity(nombreTabla):
    cuerpoClaseEntity = ""
    textoGetSet = " { get; set; }"
    tipoDato = ""
    df = obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            tipoDato = "public Int32 "
        elif (df["tipoDato"][i] == 'VARCHAR'):
            tipoDato = "public String "
        else:
            tipoDato = "public DateTime "
        cuerpoClaseEntity = cuerpoClaseEntity + ENTER + 2*TAB + tipoDato + df["nombreCampo"][i] + textoGetSet + ENTER

    return cuerpoClaseEntity

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase = cabeceraClase +"using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return nombreTabla + 'Filter'

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase
