import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoException(nombreTabla):
    rutaArchivo = generarRutaArchivo('7_EXCEPTION', enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.exception)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace " + getNombreProyecto() + "Microservice.Exceptions" + ENTER 
    claseEntity += "{" + ENTER
    claseEntity += generarCuerpoClase(nombreTabla)
    claseEntity += "}" + ENTER 

    return claseEntity

def generarCabeceraClase():
    cabeceraClase =  "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClaseEntity = ""

    cuerpoClaseEntity = cuerpoClaseEntity + TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.exception) + " : CustomException" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + TAB + "{" + ENTER 
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "public string ErrorCode { get; set; }" + 2*ENTER 
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "private List<ErrorCodeEntityException> ErrorsList = new List<ErrorCodeEntityException>() {" + ENTER 
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "new ErrorCodeEntityException { Code=\"not_found\", Message=\"No existe el objeto en la base de datos\" }" + ENTER 
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "};" + 2*ENTER    

    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "public " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.exception) + " (string errorCode)" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "{" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "this.ErrorCode = errorCode; " + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "}" + 2*ENTER

    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "public override List<string> CustomMessage" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "{" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "get" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "{" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 4*TAB + "return this.GetExceptionsList(this.ErrorCode, this.ErrorsList);" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 3*TAB + "}" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + 2*TAB + "}" + ENTER
    cuerpoClaseEntity = cuerpoClaseEntity + TAB + "}" + ENTER

    return cuerpoClaseEntity

