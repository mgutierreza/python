import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoEntity(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.entity)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace EP_AcademicMicroservice.Entities" + ENTER 
    claseEntity += "{" + ENTER
    claseEntity += TAB + "[DataContract]" + ENTER
    claseEntity += TAB + "public class " + nombreTabla + "Entity" + ENTER 
    claseEntity += TAB + "{" + ENTER 
    claseEntity += generarCuerpoClase(nombreTabla)
    claseEntity += TAB + "}" + ENTER 
    claseEntity += "}" + ENTER

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using System;" + ENTER
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.ComponentModel.DataAnnotations;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Runtime.Serialization;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 3*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClaseEntity = ""
    datamember =  "[DataMember(EmitDefaultValue = false)]"
    textoGetSet = " { get; set; }"
    
    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)

    for i in df.index:
        cuerpoClaseEntity += 2*TAB + datamember + ENTER 
        cuerpoClaseEntity += 2*TAB + "public " + df["tipoDatoNET"][i] + " " + df["nombreCampo"][i] + textoGetSet + 2*ENTER

    return cuerpoClaseEntity

