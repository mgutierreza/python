import pyodbc as pyo
import pandas as pd
from os import remove
from consultaDatos import obtenerMetaDataClavePrincipal

TAB = "\t"
ENTER = "\n"

def generarArchivoService(nombreTabla):
    clase = ""
    cabeceraClase = generarCabeceraClase()
    claseService = generarClaseService(nombreTabla)
    nombreClase = generarNombreClase(nombreTabla)
    nombreArchivo = generarNombreArchivo(nombreClase)
    clase = cabeceraClase + claseService 
    
    #remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivo,'w')
    f.write(clase)
    f.close()

    return 

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Domain;" + ENTER 
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Exceptions;" + ENTER
    cabeceraClase = cabeceraClase + "using System;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarClaseService(nombreTabla):
    claseEntity = ""
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Service" + ENTER + "{"  + ENTER   
    pieClaseEntity = "}"
    cuerpoClaseEntity = generarCuerpoClaseservice(nombreTabla)    
    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseservice(nombreTabla):
    cuerpoClase = ""
    cuerpoClase = cuerpoClase + TAB + "public class " + generarNombreClase(nombreTabla) + ENTER
    cuerpoClase = cuerpoClase + TAB + "{" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region Public Methods" + ENTER 
    cuerpoClase = cuerpoClase + generarMetodoExecute(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoGet(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoLstItemResponse(nombreTabla) + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase = cuerpoClase + TAB + "}" + ENTER
    
    return cuerpoClase

def generarMetodoExecute(nombreTabla):
    metodoExecute = ""
    campoClavePrincipal = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]

    metodoExecute = metodoExecute + 2*TAB + "public " + nombreTabla + "Response Execute(" + nombreTabla + "Request request)" + ENTER
    metodoExecute = metodoExecute + 2*TAB + "{" + ENTER 
    metodoExecute = metodoExecute + 3*TAB + nombreTabla + "Response response = new " + nombreTabla + "Response();" + ENTER 
    metodoExecute = metodoExecute + 3*TAB + "response.InitializeResponse(request);" + ENTER 
    metodoExecute = metodoExecute + 3*TAB + "try" + ENTER 
    metodoExecute = metodoExecute + 3*TAB + "{" + ENTER 
    metodoExecute = metodoExecute + 4*TAB + "if (response.LstError.Count == 0)" + ENTER 
    metodoExecute = metodoExecute + 4*TAB + "{" + ENTER 
    metodoExecute = metodoExecute + 5*TAB + "switch (request.Operation)" + ENTER 
    metodoExecute = metodoExecute + 5*TAB + "{" + ENTER 
    metodoExecute = metodoExecute + 6*TAB + "case Operation.Undefined:" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "break;" + ENTER 
    metodoExecute = metodoExecute + 6*TAB + "case Operation.Add:" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "response.Resultado = new " + nombreTabla + "Domain().Create" + nombreTabla + "(request.Item);" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "break;" + ENTER 
    metodoExecute = metodoExecute + 6*TAB + "case Operation.Edit:" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "response.Item = new " + nombreTabla + "Domain().Edit" + nombreTabla + "(request.Item);" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "break;" + ENTER 
    metodoExecute = metodoExecute + 6*TAB + "case Operation.Delete:" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "response.Item = new " + nombreTabla + "Domain().Delete" + nombreTabla + "(request.Item." + campoClavePrincipal + ");" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "break;" + ENTER 
    metodoExecute = metodoExecute + 6*TAB + "default:" + ENTER 
    metodoExecute = metodoExecute + 7*TAB + "break;" + ENTER 
    metodoExecute = metodoExecute + 5*TAB + "}" + ENTER 
    metodoExecute = metodoExecute + 5*TAB + "response.IsSuccess = true;" + ENTER 
    metodoExecute = metodoExecute + 4*TAB + "}" + ENTER 
    metodoExecute = metodoExecute + 3*TAB + "}" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "catch (CustomException ex)" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "{" + ENTER
    metodoExecute = metodoExecute + 4*TAB + "response.LstError.Add(ex.CustomMessage);" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "}" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "catch (Exception ex)" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "{" + ENTER
    metodoExecute = metodoExecute + 4*TAB + "response.LstError.Add(\"Server Error\");" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "}" + ENTER
    metodoExecute = metodoExecute + 3*TAB + "return response;" + ENTER 
    metodoExecute = metodoExecute + 2*TAB + "}" + ENTER 

    return metodoExecute

def generarMetodoGet(nombreTabla):
    metodoGet = ""
    campoClavePrincipal = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]

    metodoGet = metodoGet + 2*TAB + "public " + nombreTabla + "ItemResponse Get" + nombreTabla + "(" + nombreTabla + "ItemRequest request)" + ENTER
    metodoGet = metodoGet + 2*TAB + "{" + ENTER 
    metodoGet = metodoGet + 3*TAB + nombreTabla + "ItemResponse response = new " + nombreTabla + "ItemResponse();" + ENTER 
    metodoGet = metodoGet + 3*TAB + "response.InitializeResponse(request);" + ENTER 
    metodoGet = metodoGet + 3*TAB + "try" + ENTER 
    metodoGet = metodoGet + 3*TAB + "}" + ENTER 
    metodoGet = metodoGet + 4*TAB + "if (response.LstError.Count == 0)" + ENTER 
    metodoGet = metodoGet + 4*TAB + "{" + ENTER 
    metodoGet = metodoGet + 5*TAB + "switch (request.FilterType)" + ENTER
    metodoGet = metodoGet + 5*TAB + "{" + ENTER     
    metodoGet = metodoGet + 6*TAB + "case " + nombreTabla + "FilterItemType.ById:" + ENTER     
    metodoGet = metodoGet + 7*TAB + "response.Item = new " + nombreTabla + "Domain().GetById(request.Filter." + campoClavePrincipal + ");" + ENTER
    metodoGet = metodoGet + 7*TAB + "break;" + ENTER 
    metodoGet = metodoGet + 6*TAB + "default:" + ENTER 
    metodoGet = metodoGet + 7*TAB + "break;" + ENTER 
    metodoGet = metodoGet + 5*TAB + "}" + ENTER 
    metodoGet = metodoGet + 5*TAB + "response.IsSuccess = true;" + ENTER 
    metodoGet = metodoGet + 4*TAB + "}" + ENTER 
    metodoGet = metodoGet + 3*TAB + "}" + ENTER 
    metodoGet = metodoGet + 3*TAB + "catch (CustomException ex)" + ENTER
    metodoGet = metodoGet + 3*TAB + "{" + ENTER
    metodoGet = metodoGet + 4*TAB + "response.LstError.Add(ex.CustomMessage);" + ENTER
    metodoGet = metodoGet + 3*TAB + "}" + ENTER
    metodoGet = metodoGet + 3*TAB + "catch (Exception ex)" + ENTER
    metodoGet = metodoGet + 3*TAB + "{" + ENTER
    metodoGet = metodoGet + 4*TAB + "response.LstError.Add(\"Server Error\");" + ENTER
    metodoGet = metodoGet + 3*TAB + "}" + ENTER
    metodoGet = metodoGet + 3*TAB + "return response;" + ENTER 
    metodoGet = metodoGet + 2*TAB + "}" + ENTER 

    return metodoGet

def generarMetodoLstItemResponse(nombreTabla):
    metodoLstItemResponse = ""

    metodoLstItemResponse = metodoLstItemResponse + 2*TAB + "public " + nombreTabla + "LstItemResponse GetLst" + nombreTabla + "(" + nombreTabla + "LstItemRequest request)" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 2*TAB + "{" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + nombreTabla + "LstItemResponse response = new " + nombreTabla + "LstItemResponse();" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "response.InitializeResponse(request);" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "try" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "{" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 4*TAB + "if (response.LstError.Count == 0)" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 4*TAB + "{" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 5*TAB + "switch (request.FilterType)" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 5*TAB + "{" + ENTER     
    metodoLstItemResponse = metodoLstItemResponse + 6*TAB + "case " + nombreTabla + "FilterLstItemType.ByPagination:" + ENTER     
    metodoLstItemResponse = metodoLstItemResponse + 7*TAB + "response.Item = new " + nombreTabla + "Domain().GetByPagination(request.Filter, request.FilterType, request.Pagination);" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 7*TAB + "break;" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 6*TAB + "default:" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 7*TAB + "break;" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 5*TAB + "}" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 5*TAB + "response.IsSuccess = true;" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 4*TAB + "}" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "}" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "catch (CustomException ex)" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "{" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 4*TAB + "response.LstError.Add(ex.CustomMessage);" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "}" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "catch (Exception ex)" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "{" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 4*TAB + "response.LstError.Add(ex.Message);" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "}" + ENTER
    metodoLstItemResponse = metodoLstItemResponse + 3*TAB + "return response;" + ENTER 
    metodoLstItemResponse = metodoLstItemResponse + 2*TAB + "}" + ENTER 

    return metodoLstItemResponse

def generarNombreClase(nombreTabla):
    return nombreTabla + "Service"

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase