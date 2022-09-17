import pyodbc as pyo
import pandas as pd
from os import remove

TAB = "\t"
ENTER = "\n"

def generarArchivoRequestValidator(nombreTabla):
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
    cabeceraClaseEntity = "EP_AcademicMicroservice.Service" + ENTER + "{"  + 2*ENTER   
    pieClaseEntity = "}"

    cuerpoClaseEntity = generarCuerpoClaseRequest(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseRequest(nombreTabla):
    cuerpoClase = ""
    inicioClaseRequestValidator = ""
    finClaseRequestValidator = ""
    cuerpoPropiedadValidateRequest = ""
    cuerpoPropiedadInitializeResponse = ""
    

    inicioClaseRequestValidator = inicioClaseRequestValidator + TAB + "public static class " + nombreTabla + "RequestValidator " + ENTER
    inicioClaseRequestValidator = inicioClaseRequestValidator + TAB + "{" + 2*ENTER 
    finClaseRequestValidator = finClaseRequestValidator + TAB + "}" + 2*ENTER
    
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 2*TAB + "#region Validate" + ENTER
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 2*TAB + "public static void ValidateRequest(this " + nombreTabla + "Response response, " + nombreTabla + "Request request)" + ENTER
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 2*TAB + "{" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "if (request.Item == null)" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "{" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 4*TAB + "response.LstError.Add(\"Se requiere la entidad Estructura\");" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "}" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "if (string.IsNullOrEmpty(request.ServerName))" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "{" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 4*TAB + "response.LstError.Add(\"No se identifico el servidor de origen para la solicitud\");" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "}" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "if (string.IsNullOrEmpty(request.UserName))" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "{" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 4*TAB + "response.LstError.Add(\"No se identifico el usuario que realizo la solicitud\");" + ENTER 
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 3*TAB + "}" + ENTER
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 2*TAB + "}" + ENTER
    cuerpoPropiedadValidateRequest = cuerpoPropiedadValidateRequest + 2*TAB + "#endregion" + 2*ENTER

    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "#region Initialize" + ENTER
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "public static void InitializeResponse(this " + nombreTabla + "Response response, " + nombreTabla + "Request request)" + ENTER
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "{" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.Ticket = request.Ticket;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.ServerName = request.ServerName;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.UserName = request.UserName;" + ENTER                 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "}" + 2*ENTER             
            
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "public static void InitializeResponse(this " + nombreTabla + "ItemResponse response, " + nombreTabla + "ItemRequest request)" + ENTER
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "{" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.Ticket = request.Ticket;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.ServerName = request.ServerName;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.UserName = request.UserName;" + ENTER                 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "}" + 2*ENTER             
    
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "public static void InitializeResponse(this " + nombreTabla + "LstItemResponse response, " + nombreTabla + "LstItemRequest request)" + ENTER
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "{" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.Ticket = request.Ticket;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.ServerName = request.ServerName;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.UserName = request.UserName;" + ENTER                 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 3*TAB + "response.Pagination = request.Pagination;" + ENTER 
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "}" + ENTER             
    cuerpoPropiedadInitializeResponse = cuerpoPropiedadInitializeResponse + 2*TAB + "#endregion" + ENTER

    cuerpoClase = inicioClaseRequestValidator + cuerpoPropiedadValidateRequest + cuerpoPropiedadInitializeResponse + finClaseRequestValidator

    return cuerpoClase

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase = cabeceraClase +"using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase = cabeceraClase +"using System;" + ENTER 
    cabeceraClase = cabeceraClase +"using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return nombreTabla + 'RequestValidator'

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase