import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados
from utilitarios import util
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoService(nombreTabla):
    rutaArchivo = generarRutaArchivo('11_SERVICE', enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.service)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)
    
    return 

def generarClase(nombreTabla):
    clase = ""
    clase += generarCabeceraClase()
    clase += "namespace " + getNombreProyecto() + "Microservice.Service" + ENTER 
    clase += "{"  + ENTER   
    clase += generarCuerpoClase(nombreTabla)
    clase += "}"
    
    return clase

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using " + getNombreProyecto() + "Microservice.Domain;" + ENTER 
    cabeceraClase += "using " + getNombreProyecto() + "Microservice.Entities;" + ENTER 
    cabeceraClase += "using " + getNombreProyecto() + "Microservice.Exceptions;" + ENTER
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""
    cuerpoClase = cuerpoClase + TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.service) + ENTER
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

    df = consultaDatos.obtenerMetaDataClavePrincipal()
    for i in df.index:
        campoClavePrincipal += "request.Item." + df["nombreCampo"][i] + "," 
    
    campoClavePrincipal = util.extraerUltimoCaracter(campoClavePrincipal)

    metodoExecute += 2*TAB + "public " + nombreTabla + "Response Execute(" + nombreTabla + "Request request)" + ENTER
    metodoExecute += 2*TAB + "{" + ENTER 
    metodoExecute += 3*TAB + nombreTabla + "Response response = new " + nombreTabla + "Response();" + ENTER 
    metodoExecute += 3*TAB + "response.InitializeResponse(request);" + ENTER 
    metodoExecute += 3*TAB + "try" + ENTER 
    metodoExecute += 3*TAB + "{" + ENTER 
    metodoExecute += 4*TAB + "if (response.LstError.Count == 0)" + ENTER 
    metodoExecute += 4*TAB + "{" + ENTER 
    metodoExecute += 5*TAB + "switch (request.Operation)" + ENTER 
    metodoExecute += 5*TAB + "{" + ENTER 
    metodoExecute += 6*TAB + "case Operation.Undefined:" + ENTER 
    metodoExecute += 7*TAB + "break;" + ENTER 
    metodoExecute += 6*TAB + "case Operation.Add:" + ENTER 
    metodoExecute += 7*TAB + "response.Resultado = new " + nombreTabla + "Domain().Create" + nombreTabla + "(request.Item);" + ENTER 
    metodoExecute += 7*TAB + "break;" + ENTER 
    metodoExecute += 6*TAB + "case Operation.Edit:" + ENTER 
    metodoExecute += 7*TAB + "response.Item = new " + nombreTabla + "Domain().Edit" + nombreTabla + "(request.Item);" + ENTER 
    metodoExecute += 7*TAB + "break;" + ENTER 
    metodoExecute += 6*TAB + "case Operation.Delete:" + ENTER 
    metodoExecute += 7*TAB + "response.Item = new " + nombreTabla + "Domain().Delete" + nombreTabla + "(" + campoClavePrincipal + ");" + ENTER 
    metodoExecute += 7*TAB + "break;" + ENTER 
    metodoExecute += 6*TAB + "default:" + ENTER 
    metodoExecute += 7*TAB + "break;" + ENTER 
    metodoExecute += 5*TAB + "}" + ENTER 
    metodoExecute += 5*TAB + "response.IsSuccess = true;" + ENTER 
    metodoExecute += 4*TAB + "}" + ENTER 
    metodoExecute += 3*TAB + "}" + ENTER
    metodoExecute += 3*TAB + "catch (CustomException ex)" + ENTER
    metodoExecute += 3*TAB + "{" + ENTER
    metodoExecute += 4*TAB + "response.LstError.AddRange(ex.CustomMessage);" + ENTER
    metodoExecute += 3*TAB + "}" + ENTER
    metodoExecute += 3*TAB + "catch (Exception ex)" + ENTER
    metodoExecute += 3*TAB + "{" + ENTER
    metodoExecute += 4*TAB + "response.LstError.Add(\"Server Error\");" + ENTER
    metodoExecute += 3*TAB + "}" + ENTER
    metodoExecute += 3*TAB + "return response;" + ENTER 
    metodoExecute += 2*TAB + "}" + ENTER 

    return metodoExecute

def generarMetodoGet(nombreTabla):
    metodoGet = ""
    campoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal()
    for i in df.index:
        campoClavePrincipal += "request.Filter." + df["nombreCampo"][i] + "," 
    
    campoClavePrincipal = util.extraerUltimoCaracter(campoClavePrincipal)    

    metodoGet += 2*TAB + "public " + nombreTabla + "ItemResponse Get" + nombreTabla + "(" + nombreTabla + "ItemRequest request)" + ENTER
    metodoGet += 2*TAB + "{" + ENTER 
    metodoGet += 3*TAB + nombreTabla + "ItemResponse response = new " + nombreTabla + "ItemResponse();" + ENTER 
    metodoGet += 3*TAB + "response.InitializeResponse(request);" + ENTER 
    metodoGet += 3*TAB + "try" + ENTER 
    metodoGet += 3*TAB + "{" + ENTER 
    metodoGet += 4*TAB + "if (response.LstError.Count == 0)" + ENTER 
    metodoGet += 4*TAB + "{" + ENTER 
    metodoGet += 5*TAB + "switch (request.FilterType)" + ENTER
    metodoGet += 5*TAB + "{" + ENTER     
    metodoGet += 6*TAB + "case " + nombreTabla + "FilterItemType.ById:" + ENTER     
    metodoGet += 7*TAB + "response.Item = new " + nombreTabla + "Domain().GetById(" + campoClavePrincipal + ");" + ENTER
    metodoGet += 7*TAB + "break;" + ENTER 
    metodoGet += 6*TAB + "default:" + ENTER 
    metodoGet += 7*TAB + "break;" + ENTER 
    metodoGet += 5*TAB + "}" + ENTER 
    metodoGet += 5*TAB + "response.IsSuccess = true;" + ENTER 
    metodoGet += 4*TAB + "}" + ENTER 
    metodoGet += 3*TAB + "}" + ENTER 
    metodoGet += 3*TAB + "catch (CustomException ex)" + ENTER
    metodoGet += 3*TAB + "{" + ENTER
    metodoGet += 4*TAB + "response.LstError.AddRange(ex.CustomMessage);" + ENTER
    metodoGet += 3*TAB + "}" + ENTER
    metodoGet += 3*TAB + "catch (Exception ex)" + ENTER
    metodoGet += 3*TAB + "{" + ENTER
    metodoGet += 4*TAB + "response.LstError.Add(\"Server Error\");" + ENTER
    metodoGet += 3*TAB + "}" + ENTER
    metodoGet += 3*TAB + "return response;" + ENTER 
    metodoGet += 2*TAB + "}" + ENTER 

    return metodoGet

def generarMetodoLstItemResponse(nombreTabla):
    metodoLstItemResponse = ""

    metodoLstItemResponse += 2*TAB + "public " + nombreTabla + "LstItemResponse GetLst" + nombreTabla + "(" + nombreTabla + "LstItemRequest request)" + ENTER
    metodoLstItemResponse += 2*TAB + "{" + ENTER 
    metodoLstItemResponse += 3*TAB + nombreTabla + "LstItemResponse response = new " + nombreTabla + "LstItemResponse();" + ENTER 
    metodoLstItemResponse += 3*TAB + "response.InitializeResponse(request);" + ENTER 
    metodoLstItemResponse += 3*TAB + "try" + ENTER 
    metodoLstItemResponse += 3*TAB + "{" + ENTER 
    metodoLstItemResponse += 4*TAB + "if (response.LstError.Count == 0)" + ENTER 
    metodoLstItemResponse += 4*TAB + "{" + ENTER 
    metodoLstItemResponse += 5*TAB + "switch (request.FilterType)" + ENTER
    metodoLstItemResponse += 5*TAB + "{" + ENTER     
    metodoLstItemResponse += 6*TAB + "case " + nombreTabla + "FilterLstItemType.ByPagination:" + ENTER     
    metodoLstItemResponse += 7*TAB + "response.LstItem = new " + nombreTabla + "Domain().GetByPagination(request.Filter, request.FilterType, request.Pagination);" + ENTER
    metodoLstItemResponse += 7*TAB + "break;" + ENTER 
    metodoLstItemResponse += 6*TAB + "default:" + ENTER 
    metodoLstItemResponse += 7*TAB + "break;" + ENTER 
    metodoLstItemResponse += 5*TAB + "}" + ENTER 
    metodoLstItemResponse += 5*TAB + "response.IsSuccess = true;" + ENTER 
    metodoLstItemResponse += 4*TAB + "}" + ENTER 
    metodoLstItemResponse += 3*TAB + "}" + ENTER 
    metodoLstItemResponse += 3*TAB + "catch (CustomException ex)" + ENTER
    metodoLstItemResponse += 3*TAB + "{" + ENTER
    metodoLstItemResponse += 4*TAB + "response.LstError.AddRange(ex.CustomMessage);" + ENTER
    metodoLstItemResponse += 3*TAB + "}" + ENTER
    metodoLstItemResponse += 3*TAB + "catch (Exception ex)" + ENTER
    metodoLstItemResponse += 3*TAB + "{" + ENTER
    metodoLstItemResponse += 4*TAB + "response.LstError.Add(ex.Message);" + ENTER
    metodoLstItemResponse += 3*TAB + "}" + ENTER
    metodoLstItemResponse += 3*TAB + "return response;" + ENTER 
    metodoLstItemResponse += 2*TAB + "}" + ENTER 

    return metodoLstItemResponse
