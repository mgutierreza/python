import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoFilter(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.filter)
    extensionArchivo = generarExtensionArchivo(tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return

def generarClase(nombreTabla):
    clase = ""
    clase += generarCabeceraClase()
    clase += "namespace EP_AcademicMicroservice.Entities" + ENTER 
    clase += "{" + ENTER
    clase += TAB + "public class " + generarNombreArchivo(nombreTabla, claseObjeto.filter) + ENTER 
    clase += TAB + "{" 
    clase += generarCuerpoClase(nombreTabla)
    clase += TAB + "}" + ENTER 
    clase += "}" + ENTER

    return clase

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase = cabeceraClase +"using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER

    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""
    textoGetSet = " { get; set; }"
    tipoDato = ""
    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            tipoDato = "public Int32 "
        elif (df["tipoDato"][i] == 'VARCHAR'):
            tipoDato = "public String "
        else:
            tipoDato = "public DateTime "
        cuerpoClase += 2*TAB + tipoDato + df["nombreCampo"][i] + textoGetSet + ENTER

    return cuerpoClase
