import pyodbc as pyo
import pandas as pd
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoResponse(nombreTabla):
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
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Entities" + ENTER + "{"  + 2*ENTER   
    pieClaseEntity = "}"

    cuerpoClaseEntity = generarCuerpoClaseRequest(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseRequest(nombreTabla):
    cuerpoClase = ""
    cuerpoClaseRequest = ""
    cuerpoClaseItemRequest = ""
    cuerpoClaseLstItemRequest = ""

    cuerpoClaseRequest = cuerpoClaseRequest + TAB + "public class " + nombreTabla + "Response : ItemResponse<bool>" + ENTER
    cuerpoClaseRequest = cuerpoClaseRequest + TAB + "{" + 2*ENTER 
    cuerpoClaseRequest = cuerpoClaseRequest + TAB + "}" + 2*ENTER
    
    cuerpoClaseItemRequest = cuerpoClaseItemRequest + TAB + "public class " + nombreTabla + "ItemResponse : ItemResponse<" + nombreTabla + "Entity>" + ENTER
    cuerpoClaseItemRequest = cuerpoClaseItemRequest + TAB + "{" + 2*ENTER 
    cuerpoClaseItemRequest = cuerpoClaseItemRequest + TAB + "}" + 2*ENTER

    cuerpoClaseLstItemRequest = cuerpoClaseLstItemRequest + TAB + "public class " + nombreTabla + "LstItemResponse : LstItemResponse<" + nombreTabla + "Entity>" + ENTER
    cuerpoClaseLstItemRequest = cuerpoClaseLstItemRequest + TAB + "{" + 2*ENTER 
    cuerpoClaseLstItemRequest = cuerpoClaseLstItemRequest + TAB + "}" + 2*ENTER


    cuerpoClase = cuerpoClaseRequest + cuerpoClaseItemRequest + cuerpoClaseLstItemRequest

    return cuerpoClase

def generarCabeceraClase():
    cabeceraClase = "using System;" + ENTER 
    cabeceraClase = cabeceraClase +"using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return nombreTabla + 'Response'

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase