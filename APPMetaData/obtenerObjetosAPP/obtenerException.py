import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoException(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.exception)
    extensionArchivo = generarExtensionArchivo(tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace EP_AcademicMicroservice.Exceptions" + ENTER 
    claseEntity += "{" + ENTER
    claseEntity += generarCuerpoClase(nombreTabla)
    claseEntity += "}" + ENTER 

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClaseEntity = ""

    cuerpoClaseEntity = cuerpoClaseEntity + TAB + "public class " + generarNombreArchivo(nombreTabla, claseObjeto.exception) + " : CustomException" + ENTER
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

