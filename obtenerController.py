import pyodbc as pyo
import pandas as pd
import os
from os import remove
from consultaDatos import obtenerMetaDataClavePrincipal
from crearArchivo import generarArchivo

TAB = "\t"
ENTER = "\n"

def generarArchivoController(nombreTabla):
    cabeceraClase = generarCabeceraClase()
    claseController = generarClaseController(nombreTabla)
    nombreArchivo = generarNombreClase(nombreTabla)
    contenidoArchivo = cabeceraClase + claseController 
    generarArchivo(nombreTabla, nombreArchivo, contenidoArchivo)
    
    return 

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Service;" + ENTER 
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase = cabeceraClase + "using Microsoft.AspNetCore.Mvc;" + ENTER
    cabeceraClase = cabeceraClase + "using System;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + 2*ENTER

    return cabeceraClase

    
def generarClaseController(nombreTabla):
    claseEntity = ""
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Api.Controllers" + ENTER + "{"  + ENTER   
    pieClaseEntity = "}"
    cuerpoClaseEntity = generarCuerpoClaseController(nombreTabla)    
    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseController(nombreTabla):
    cuerpoClase = ""

    cuerpoClase = cuerpoClase + TAB + "[Route(\"api/[controller]\")]" + ENTER
    cuerpoClase = cuerpoClase + TAB + "[ApiController]" + ENTER
    cuerpoClase = cuerpoClase + TAB + "public class " + generarNombreClase(nombreTabla) + " : ControllerBase" + ENTER
    cuerpoClase = cuerpoClase + TAB + "{" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region Operations" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "[HttpGet(\"GetByPagination\", Name = \"" + nombreTabla + "_GetByPagination\")]" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "[ProducesResponseType(200)]" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "[ProducesResponseType(400)]" + ENTER 
    cuerpoClase = cuerpoClase + generarMetodoObtenerByPagination(nombreTabla) + 2*ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "[HttpGet(\"{Id}\", Name = \"" + nombreTabla + "_GetById\")]" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "[ProducesResponseType(200)]" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "[ProducesResponseType(400)]" + ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "[ProducesResponseType(404)]" + ENTER
    cuerpoClase = cuerpoClase + generarMetodoObtenerByID(nombreTabla) + 2*ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "[HttpPost(\"Insert\")]" + ENTER
    cuerpoClase = cuerpoClase + generarMetodoPost(nombreTabla) + 2*ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "[HttpPost(\"update\")]" + ENTER
    cuerpoClase = cuerpoClase + generarMetodoUpdate(nombreTabla) + 2*ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "[HttpPost(\"Delete\")]" + ENTER
    cuerpoClase = cuerpoClase + generarMetodoDelete(nombreTabla) + 2*ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + ENTER 
    cuerpoClase = cuerpoClase + TAB + "}" + ENTER
    
    return cuerpoClase

def generarMetodoObtenerByPagination(nombreTabla):
    MetodoObtenerByPagination = ""

    MetodoObtenerByPagination = MetodoObtenerByPagination + 2*TAB + "public IActionResult GetByPagination()" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 2*TAB + "{" + ENTER 
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + nombreTabla + "LstItemResponse response = null;" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + nombreTabla + "LstItemRequest request = new " + nombreTabla + "LstItemRequest()" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "{" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 4*TAB + "Filter = new " + nombreTabla + "Filter() { }," + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 4*TAB + "FilterType = " + nombreTabla + "FilterLstItemType.ByPagination" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "};" + 2*ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "try" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "{" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 4*TAB + "response = new " + nombreTabla + "Service().GetLst" + nombreTabla + "(request);" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 4*TAB + "if (!response.IsSuccess)" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 5*TAB + "return BadRequest(response);" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "}" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "catch (Exception)" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "{" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 4*TAB + "throw;" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "}" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "return Ok(response);" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 2*TAB + "}" + ENTER

    return MetodoObtenerByPagination

def generarMetodoObtenerByID(nombreTabla):
    metodoObtenerByID = ""
    tipoDatoClavePrincipal = ""
    nombreCampoClavePrincipal = ""
    tipoDato = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDato"][i]
        nombreCampoClavePrincipal = df["nombreCampo"][i]
    
    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "Int32"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "String"
    else:
        tipoDato = "DateTime"

    metodoObtenerByID = metodoObtenerByID + 2*TAB + "public IActionResult GetById(" + tipoDato + " Id)" + ENTER
    metodoObtenerByID = metodoObtenerByID + 2*TAB + "{" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + nombreTabla + "ItemResponse response = null;" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + nombreTabla + "ItemRequest request = new " + nombreTabla + "ItemRequest()" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "{" + ENTER
    metodoObtenerByID = metodoObtenerByID + 4*TAB + "Filter = new " + nombreTabla + "Filter() { " + nombreCampoClavePrincipal + " = Id }," + ENTER
    metodoObtenerByID = metodoObtenerByID + 4*TAB + "FilterType = " + nombreTabla + "FilterItemType.ById" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "};" + 2*ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "try" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "{" + ENTER
    metodoObtenerByID = metodoObtenerByID + 4*TAB + "response = new " + nombreTabla + "Service().Get" + nombreTabla + "(request);" + ENTER
    metodoObtenerByID = metodoObtenerByID + 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoObtenerByID = metodoObtenerByID + 5*TAB + "return BadRequest(response);" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "}" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "catch (Exception)" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "{" + ENTER
    metodoObtenerByID = metodoObtenerByID + 4*TAB + "throw;" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "}" + ENTER
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "return Ok(response);" + ENTER
    metodoObtenerByID = metodoObtenerByID + 2*TAB + "}" + ENTER

    return metodoObtenerByID

def generarMetodoPost(nombreTabla):
    metodoPost = ""

    metodoPost = metodoPost + 2*TAB + "public IActionResult Post([FromBody] " + nombreTabla + "Entity Estructura)" + ENTER
    metodoPost = metodoPost + 2*TAB + "{" + ENTER 
    metodoPost = metodoPost + 3*TAB + nombreTabla + "Response response = null;" + ENTER
    metodoPost = metodoPost + 3*TAB + nombreTabla + "Request request = new " + nombreTabla + "Request()" + ENTER
    metodoPost = metodoPost + 3*TAB + "{" + ENTER
    metodoPost = metodoPost + 4*TAB + "Item = Estructura," + ENTER
    metodoPost = metodoPost + 4*TAB + "Operation = Operation.Add" + ENTER
    metodoPost = metodoPost + 3*TAB + "};" + 2*ENTER
    metodoPost = metodoPost + 3*TAB + "try" + ENTER
    metodoPost = metodoPost + 3*TAB + "{" + ENTER
    metodoPost = metodoPost + 4*TAB + "response = new " + nombreTabla + "Service().Execute(request);" + ENTER
    metodoPost = metodoPost + 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoPost = metodoPost + 5*TAB + "return BadRequest(response);" + ENTER
    metodoPost = metodoPost + 3*TAB + "}" + ENTER
    metodoPost = metodoPost + 3*TAB + "catch (Exception)" + ENTER
    metodoPost = metodoPost + 3*TAB + "{" + ENTER
    metodoPost = metodoPost + 4*TAB + "throw;" + ENTER
    metodoPost = metodoPost + 3*TAB + "}" + ENTER
    metodoPost = metodoPost + 3*TAB + "return Ok(response);" + ENTER
    metodoPost = metodoPost + 2*TAB + "}" + ENTER

    return metodoPost    


def generarMetodoUpdate(nombreTabla):
    metodoUpdate = ""

    metodoUpdate = metodoUpdate + 2*TAB + "public IActionResult Put([FromBody] " + nombreTabla + "Entity Estructura)" + ENTER
    metodoUpdate = metodoUpdate + 2*TAB + "{" + ENTER 
    metodoUpdate = metodoUpdate + 3*TAB + nombreTabla + "Response response = null;" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + nombreTabla + "Request request = new " + nombreTabla + "Request()" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "{" + ENTER
    metodoUpdate = metodoUpdate + 4*TAB + "Item = Estructura," + ENTER
    metodoUpdate = metodoUpdate + 4*TAB + "Operation = Operation.Edit" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "};" + 2*ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "try" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "{" + ENTER
    metodoUpdate = metodoUpdate + 4*TAB + "response = new " + nombreTabla + "Service().Execute(request);" + ENTER
    metodoUpdate = metodoUpdate + 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoUpdate = metodoUpdate + 5*TAB + "return BadRequest(response);" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "}" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "catch (Exception)" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "{" + ENTER
    metodoUpdate = metodoUpdate + 4*TAB + "throw;" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "}" + ENTER
    metodoUpdate = metodoUpdate + 3*TAB + "return Ok(response);" + ENTER
    metodoUpdate = metodoUpdate + 2*TAB + "}" + ENTER

    return metodoUpdate    

def generarMetodoDelete(nombreTabla):
    metodoDelete = ""
    tipoDatoClavePrincipal = ""
    nombreCampoClavePrincipal = ""
    tipoDato = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDato"][i]
        nombreCampoClavePrincipal = df["nombreCampo"][i]
    
    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "Int32"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "String"
    else:
        tipoDato = "DateTime"

    metodoDelete = metodoDelete + 2*TAB + "public IActionResult Delete(" + tipoDato + " Id)" + ENTER
    metodoDelete = metodoDelete + 2*TAB + "{" + ENTER 
    metodoDelete = metodoDelete + 3*TAB + nombreTabla + "Response response = null;" + ENTER
    metodoDelete = metodoDelete + 3*TAB + nombreTabla + "Request request = new " + nombreTabla + "Request()" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "{" + ENTER
    metodoDelete = metodoDelete + 4*TAB + "Item = new " + nombreTabla + "Entity() { " + nombreCampoClavePrincipal + " = Id }," + ENTER
    metodoDelete = metodoDelete + 4*TAB + "Operation = Operation.Delete" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "};" + 2*ENTER
    metodoDelete = metodoDelete + 3*TAB + "try" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "{" + ENTER
    metodoDelete = metodoDelete + 4*TAB + "response = new " + nombreTabla + "Service().Execute(request);" + ENTER
    metodoDelete = metodoDelete + 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoDelete = metodoDelete + 5*TAB + "return BadRequest(response);" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "}" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "catch (Exception)" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "{" + ENTER
    metodoDelete = metodoDelete + 4*TAB + "throw;" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "}" + ENTER
    metodoDelete = metodoDelete + 3*TAB + "return Ok(response);" + ENTER
    metodoDelete = metodoDelete + 2*TAB + "}" + ENTER
    
    return metodoDelete

def generarNombreClase(nombreTabla):
    return nombreTabla + "Controller"