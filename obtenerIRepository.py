import pyodbc as pyo
import pandas as pd
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoIRepository(nombreTabla):
    clase = ""
    cabeceraClase = generarCabeceraClase()
    claseRequest = generarClaseRequest(nombreTabla)
    nombreClase = generarNombreClase(nombreTabla)
    nombreArchivo = generarNombreArchivo(nombreClase)
    clase = cabeceraClase + claseRequest 
    
    #remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivo,'w')
    f.write(clase)
    f.close()

    return 

def generarClaseRequest(nombreTabla):
    claseEntity = ""
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Repository" + ENTER + "{"  + ENTER   
    pieClaseEntity = "}"

    cuerpoClaseEntity = generarCuerpoClaseRequest(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseRequest(nombreTabla):
    cuerpoClase = ""

    cuerpoClase = cuerpoClase + TAB + "public interface " + generarNombreClase(nombreTabla) + " : IGenericRepository<" + nombreTabla + "Entity>" + ENTER
    cuerpoClase = cuerpoClase + TAB + "{" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "int Insert" + nombreTabla + "(" + nombreTabla + "Entity item);" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "bool Update" + nombreTabla + "(" + nombreTabla + "Entity item);" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "bool Delete" + nombreTabla + "(int Id);" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + nombreTabla + "Entity GetItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterItemType filterType);" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "IEnumerable<" + nombreTabla + "Entity> GetLstItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterLstItemType filterType, Pagination pagination);" + ENTER 
    cuerpoClase = cuerpoClase + TAB + "}" + ENTER
    
    return cuerpoClase

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase = cabeceraClase + "using System;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return "I" + nombreTabla + "Repository"

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase