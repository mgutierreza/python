import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoFilterType(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.filterType)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return

def generarClase(nombreTabla):
    clase = ""
    clase += generarCabeceraClase() + ENTER
    clase += "namespace " + getNombreProyecto() + "Microservice.Entities" + ENTER 
    clase += "{" + ENTER
    clase += generarCuerpoClase(nombreTabla)    
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

    cuerpoClase += ENTER + TAB + "public enum " + nombreTabla + "FilterItemType : byte" + ENTER
    cuerpoClase += TAB + "{" + ENTER 
    cuerpoClase += 2*TAB + "Undefined," + ENTER
    cuerpoClase += 2*TAB + "ById" + ENTER
    cuerpoClase += TAB + "}" + 2*ENTER

    cuerpoClase += TAB + "public enum " + nombreTabla + "FilterLstItemType : byte" + ENTER
    cuerpoClase += TAB + "{" + ENTER 
    cuerpoClase += 2*TAB + "Undefined," + ENTER
    cuerpoClase += 2*TAB + "ByPagination" + ENTER
    cuerpoClase += TAB + "}" + ENTER

    return cuerpoClase

