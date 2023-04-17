import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoFilter(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.filter)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return

def generarClase(nombreTabla):
    clase = ""
    clase += generarCabeceraClase()
    clase += "namespace " + getNombreProyecto() + "Microservice.Entities" + ENTER 
    clase += "{" + ENTER
    clase += TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.filter) + ENTER 
    clase += TAB + "{" + ENTER
    clase += generarCuerpoClase(nombreTabla)
    clase += TAB + "}" + ENTER 
    clase += "}" + ENTER

    return clase

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER

    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""
    textoGetSet = " { get; set; }"
    tipoDato = ""
    df = consultaDatos.obtenerMetaDataClaves(nombreTabla)

    for i in df.index:
        tipoDato = df["tipoDatoNET"][i]
        cuerpoClase += 2*TAB + "public " + tipoDato + " " + df["nombreCampo"][i] + textoGetSet + ENTER

    return cuerpoClase
