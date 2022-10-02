import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoIRepository(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.iRepository)
    extensionArchivo = generarExtensionArchivo(tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace EP_AcademicMicroservice.Repository" + ENTER 
    claseEntity += "{"  + ENTER   
    claseEntity += generarCuerpoClase(nombreTabla)    
    claseEntity += "}"

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""

    cuerpoClase += TAB + "public interface " + generarNombreArchivo(nombreTabla, claseObjeto.iRepository) + " : IGenericRepository<" + nombreTabla + "Entity>" + ENTER
    cuerpoClase += TAB + "{" + ENTER 
    cuerpoClase += 2*TAB + "int Insert" + nombreTabla + "(" + nombreTabla + "Entity item);" + ENTER 
    cuerpoClase += 2*TAB + "bool Update" + nombreTabla + "(" + nombreTabla + "Entity item);" + ENTER 
    cuerpoClase += 2*TAB + "bool Delete" + nombreTabla + "(int Id);" + ENTER 
    cuerpoClase += 2*TAB + nombreTabla + "Entity GetItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterItemType filterType);" + ENTER 
    cuerpoClase += 2*TAB + "IEnumerable<" + nombreTabla + "Entity> GetLstItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterLstItemType filterType, Pagination pagination);" + ENTER 
    cuerpoClase += TAB + "}" + ENTER
    
    return cuerpoClase
