import pyodbc as pyonsultaDatos
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoController(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.controller)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)
    
    return 

def generarClase(nombreTabla):
    clase = ""
    clase += generarCabeceraClase()
    clase += "namespace EP_AcademicMicroservice.Api.Controllers" + ENTER 
    clase += "{"  + ENTER   
    clase += generarCuerpoClase(nombreTabla)    
    clase += "}"

    return clase

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using EP_AcademicMicroservice.Service;" + ENTER 
    cabeceraClase += "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase += "using Microsoft.AspNetCore.Mvc;" + ENTER
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER

    return cabeceraClase
 
def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""
    nombreCampoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        nombreCampoClavePrincipal = df["nombreCampo"][i]

    cuerpoClase += TAB + "[Route(\"api/[controller]\")]" + ENTER
    cuerpoClase += TAB + "[ApiController]" + ENTER
    cuerpoClase += TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.controller) + " : ControllerBase" + ENTER
    cuerpoClase += TAB + "{" + ENTER 
    cuerpoClase += 2*TAB + "#region Operations" + ENTER 
    cuerpoClase += 2*TAB + "[HttpGet(\"GetByPagination/{" + nombreCampoClavePrincipal + "}\", Name = \"" + nombreTabla + "_GetByPagination\")]" + ENTER 
    cuerpoClase += 2*TAB + "[ProducesResponseType(200)]" + ENTER 
    cuerpoClase += 2*TAB + "[ProducesResponseType(400)]" + ENTER 
    cuerpoClase += generarMetodoObtenerByPagination(nombreTabla) + 2*ENTER
    cuerpoClase += 2*TAB + "[HttpGet(\"{" + nombreCampoClavePrincipal + "}\", Name = \"" + nombreTabla + "_GetById\")]" + ENTER 
    cuerpoClase += 2*TAB + "[ProducesResponseType(200)]" + ENTER 
    cuerpoClase += 2*TAB + "[ProducesResponseType(400)]" + ENTER
    cuerpoClase += 2*TAB + "[ProducesResponseType(404)]" + ENTER
    cuerpoClase += generarMetodoObtenerByID(nombreTabla) + 2*ENTER
    cuerpoClase += 2*TAB + "[HttpPost(\"Insert\")]" + ENTER
    cuerpoClase += generarMetodoPost(nombreTabla) + 2*ENTER
    cuerpoClase += 2*TAB + "[HttpPost(\"update\")]" + ENTER
    cuerpoClase += generarMetodoUpdate(nombreTabla) + 2*ENTER
    cuerpoClase += 2*TAB + "[HttpPost(\"Delete\")]" + ENTER
    cuerpoClase += generarMetodoDelete(nombreTabla) + 2*ENTER
    cuerpoClase += 2*TAB + "#endregion" + ENTER 
    cuerpoClase += TAB + "}" + ENTER
    
    return cuerpoClase

def generarMetodoObtenerByPagination(nombreTabla):
    MetodoObtenerByPagination = ""
    tipoDatoClavePrincipal = ""
    nombreCampoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
        nombreCampoClavePrincipal = df["nombreCampo"][i]

    MetodoObtenerByPagination += 2*TAB + "public IActionResult GetByPagination(" + tipoDatoClavePrincipal + " " + nombreCampoClavePrincipal + ")" + ENTER
    MetodoObtenerByPagination += 2*TAB + "{" + ENTER 
    MetodoObtenerByPagination += 3*TAB + nombreTabla + "LstItemResponse response = null;" + ENTER
    MetodoObtenerByPagination += 3*TAB + nombreTabla + "LstItemRequest request = new " + nombreTabla + "LstItemRequest()" + ENTER
    MetodoObtenerByPagination += 3*TAB + "{" + ENTER
    MetodoObtenerByPagination += 4*TAB + "Filter = new " + nombreTabla + "Filter() { }," + ENTER
    MetodoObtenerByPagination += 4*TAB + "FilterType = " + nombreTabla + "FilterLstItemType.ByPagination" + ENTER
    MetodoObtenerByPagination += 3*TAB + "};" + 2*ENTER
    MetodoObtenerByPagination += 3*TAB + "try" + ENTER
    MetodoObtenerByPagination += 3*TAB + "{" + ENTER
    MetodoObtenerByPagination += 4*TAB + "response = new " + nombreTabla + "Service().GetLst" + nombreTabla + "(request);" + ENTER
    MetodoObtenerByPagination += 4*TAB + "if (!response.IsSuccess)" + ENTER
    MetodoObtenerByPagination += 5*TAB + "return BadRequest(response);" + ENTER
    MetodoObtenerByPagination += 3*TAB + "}" + ENTER
    MetodoObtenerByPagination += 3*TAB + "catch (Exception)" + ENTER
    MetodoObtenerByPagination += 3*TAB + "{" + ENTER
    MetodoObtenerByPagination += 4*TAB + "throw;" + ENTER
    MetodoObtenerByPagination += 3*TAB + "}" + ENTER
    MetodoObtenerByPagination += 3*TAB + "return Ok(response);" + ENTER
    MetodoObtenerByPagination += 2*TAB + "}" + ENTER

    return MetodoObtenerByPagination

def generarMetodoObtenerByID(nombreTabla):
    metodoObtenerByID = ""
    tipoDatoClavePrincipal = ""
    nombreCampoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
        nombreCampoClavePrincipal = df["nombreCampo"][i]
    
    metodoObtenerByID += 2*TAB + "public IActionResult GetById(" + tipoDatoClavePrincipal + " " + nombreCampoClavePrincipal + ")" + ENTER
    metodoObtenerByID += 2*TAB + "{" + ENTER 
    metodoObtenerByID += 3*TAB + nombreTabla + "ItemResponse response = null;" + ENTER
    metodoObtenerByID += 3*TAB + nombreTabla + "ItemRequest request = new " + nombreTabla + "ItemRequest()" + ENTER
    metodoObtenerByID += 3*TAB + "{" + ENTER
    metodoObtenerByID += 4*TAB + "Filter = new " + nombreTabla + "Filter() { " + nombreCampoClavePrincipal + " = " + nombreCampoClavePrincipal + " }," + ENTER
    metodoObtenerByID += 4*TAB + "FilterType = " + nombreTabla + "FilterItemType.ById" + ENTER
    metodoObtenerByID += 3*TAB + "};" + 2*ENTER
    metodoObtenerByID += 3*TAB + "try" + ENTER
    metodoObtenerByID += 3*TAB + "{" + ENTER
    metodoObtenerByID += 4*TAB + "response = new " + nombreTabla + "Service().Get" + nombreTabla + "(request);" + ENTER
    metodoObtenerByID += 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoObtenerByID += 5*TAB + "return BadRequest(response);" + ENTER
    metodoObtenerByID += 3*TAB + "}" + ENTER
    metodoObtenerByID += 3*TAB + "catch (Exception)" + ENTER
    metodoObtenerByID += 3*TAB + "{" + ENTER
    metodoObtenerByID += 4*TAB + "throw;" + ENTER
    metodoObtenerByID += 3*TAB + "}" + ENTER
    metodoObtenerByID += 3*TAB + "return Ok(response);" + ENTER
    metodoObtenerByID += 2*TAB + "}" + ENTER

    return metodoObtenerByID

def generarMetodoPost(nombreTabla):
    metodoPost = ""

    metodoPost += 2*TAB + "public IActionResult Post([FromBody] " + nombreTabla + "Entity Estructura)" + ENTER
    metodoPost += 2*TAB + "{" + ENTER 
    metodoPost += 3*TAB + nombreTabla + "Response response = null;" + ENTER
    metodoPost += 3*TAB + nombreTabla + "Request request = new " + nombreTabla + "Request()" + ENTER
    metodoPost += 3*TAB + "{" + ENTER
    metodoPost += 4*TAB + "Item = Estructura," + ENTER
    metodoPost += 4*TAB + "Operation = Operation.Add" + ENTER
    metodoPost += 3*TAB + "};" + 2*ENTER
    metodoPost += 3*TAB + "try" + ENTER
    metodoPost += 3*TAB + "{" + ENTER
    metodoPost += 4*TAB + "response = new " + nombreTabla + "Service().Execute(request);" + ENTER
    metodoPost += 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoPost += 5*TAB + "return BadRequest(response);" + ENTER
    metodoPost += 3*TAB + "}" + ENTER
    metodoPost += 3*TAB + "catch (Exception)" + ENTER
    metodoPost += 3*TAB + "{" + ENTER
    metodoPost += 4*TAB + "throw;" + ENTER
    metodoPost += 3*TAB + "}" + ENTER
    metodoPost += 3*TAB + "return Ok(response);" + ENTER
    metodoPost += 2*TAB + "}" + ENTER

    return metodoPost    

def generarMetodoUpdate(nombreTabla):
    metodoUpdate = ""

    metodoUpdate += 2*TAB + "public IActionResult Put([FromBody] " + nombreTabla + "Entity Estructura)" + ENTER
    metodoUpdate += 2*TAB + "{" + ENTER 
    metodoUpdate += 3*TAB + nombreTabla + "Response response = null;" + ENTER
    metodoUpdate += 3*TAB + nombreTabla + "Request request = new " + nombreTabla + "Request()" + ENTER
    metodoUpdate += 3*TAB + "{" + ENTER
    metodoUpdate += 4*TAB + "Item = Estructura," + ENTER
    metodoUpdate += 4*TAB + "Operation = Operation.Edit" + ENTER
    metodoUpdate += 3*TAB + "};" + 2*ENTER
    metodoUpdate += 3*TAB + "try" + ENTER
    metodoUpdate += 3*TAB + "{" + ENTER
    metodoUpdate += 4*TAB + "response = new " + nombreTabla + "Service().Execute(request);" + ENTER
    metodoUpdate += 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoUpdate += 5*TAB + "return BadRequest(response);" + ENTER
    metodoUpdate += 3*TAB + "}" + ENTER
    metodoUpdate += 3*TAB + "catch (Exception)" + ENTER
    metodoUpdate += 3*TAB + "{" + ENTER
    metodoUpdate += 4*TAB + "throw;" + ENTER
    metodoUpdate += 3*TAB + "}" + ENTER
    metodoUpdate += 3*TAB + "return Ok(response);" + ENTER
    metodoUpdate += 2*TAB + "}" + ENTER

    return metodoUpdate    

def generarMetodoDelete(nombreTabla):
    metodoDelete = ""
    tipoDatoClavePrincipal = ""
    nombreCampoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
        nombreCampoClavePrincipal = df["nombreCampo"][i]

    metodoDelete += 2*TAB + "public IActionResult Delete(" + tipoDatoClavePrincipal + " " + nombreCampoClavePrincipal + ")" + ENTER
    metodoDelete += 2*TAB + "{" + ENTER 
    metodoDelete += 3*TAB + nombreTabla + "Response response = null;" + ENTER
    metodoDelete += 3*TAB + nombreTabla + "Request request = new " + nombreTabla + "Request()" + ENTER
    metodoDelete += 3*TAB + "{" + ENTER
    metodoDelete += 4*TAB + "Item = new " + nombreTabla + "Entity() { " + nombreCampoClavePrincipal + " = " + nombreCampoClavePrincipal + " }," + ENTER
    metodoDelete += 4*TAB + "Operation = Operation.Delete" + ENTER
    metodoDelete += 3*TAB + "};" + 2*ENTER
    metodoDelete += 3*TAB + "try" + ENTER
    metodoDelete += 3*TAB + "{" + ENTER
    metodoDelete += 4*TAB + "response = new " + nombreTabla + "Service().Execute(request);" + ENTER
    metodoDelete += 4*TAB + "if (!response.IsSuccess)" + ENTER
    metodoDelete += 5*TAB + "return BadRequest(response);" + ENTER
    metodoDelete += 3*TAB + "}" + ENTER
    metodoDelete += 3*TAB + "catch (Exception)" + ENTER
    metodoDelete += 3*TAB + "{" + ENTER
    metodoDelete += 4*TAB + "throw;" + ENTER
    metodoDelete += 3*TAB + "}" + ENTER
    metodoDelete += 3*TAB + "return Ok(response);" + ENTER
    metodoDelete += 2*TAB + "}" + ENTER
    
    return metodoDelete

