import pyodbc as pyo
import pandas as pd
from consultaDatos import obtenerMetaDataCampos
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoEntity(nombreTabla):
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
    cabeceraClaseEntity = cabeceraClaseEntity + TAB + "[DataContract]" + ENTER
    cabeceraClaseEntity = cabeceraClaseEntity + TAB + "public class AcdCampusEntity" + ENTER + TAB + "{" + 2*ENTER 
    pieClaseEntity = TAB + "}" + ENTER + "}" + ENTER

    cuerpoClaseEntity = generarCuerpoClaseEntity(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER + "using System.Collections.Generic;" + ENTER + "using System.ComponentModel.DataAnnotations;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER + "using System.Runtime.Serialization;" + ENTER + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 3*ENTER
    return cabeceraClase

def generarCuerpoClaseEntity(nombreTabla):
    cuerpoClaseEntity = ""
    cabeceraPropiedad = "[DataMember(EmitDefaultValue = false)]"
    textoGetSet = " { get; set; }"
    tipoDato = ""
    df = obtenerMetaDataCampos(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            tipoDato = "public Int32 "
        elif (df["tipoDato"][i] == 'VARCHAR'):
            tipoDato = "public String "
        else:
            tipoDato = "public DateTime "
        cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + cabeceraPropiedad + ENTER + 2*TAB + tipoDato + df["nombreCampo"][i] + textoGetSet + 2*ENTER

    return cuerpoClaseEntity

def generarNombreClase(nombreTabla):
    return nombreTabla + 'Entity'

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase
