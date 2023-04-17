import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoDomain(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.domain)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarClase(nombreTabla):
    clase = ""
    clase += generarCabeceraClase()
    clase += "namespace " + getNombreProyecto() + "Microservice.Domain" + ENTER 
    clase += "{"  + ENTER   
    clase += generarCuerpoClase(nombreTabla)
    clase += "}"

    return clase

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using EP_AcademicMicroservice.Repository;" + ENTER 
    cabeceraClase += "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Composition;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + ENTER
    cabeceraClase += "using System.Transactions;" + ENTER
    cabeceraClase += "using Util;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""
    cuerpoClase += TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.domain) + ENTER
    cuerpoClase += TAB + "{" + ENTER 
    cuerpoClase += 2*TAB + "#region MEF" + ENTER 
    cuerpoClase += 2*TAB + "[Import]" + ENTER 
    cuerpoClase += 2*TAB + "private I" + nombreTabla + "Repository _" + nombreTabla + "Repository { get; set; }" + ENTER 
    cuerpoClase += 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase += 2*TAB + "#region Constructor" + 2*ENTER 
    cuerpoClase += generarConstructorClase(nombreTabla) + ENTER 
    cuerpoClase += 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase += 2*TAB + "#region Methods Public" + 2*ENTER 
    cuerpoClase += generarMetodoCreate(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoEdit(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoDelete(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoObtenerByID(nombreTabla) + 2*ENTER
    cuerpoClase += generarMetodoObtenerByPagination(nombreTabla) + ENTER
    cuerpoClase += 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase += TAB + "}" + ENTER
    
    return cuerpoClase

def generarConstructorClase(nombreTabla):
    constructorClase = ""
    constructorClase += 2*TAB + "public " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.domain) + "()" + ENTER
    constructorClase += 2*TAB + "{" + ENTER
    constructorClase += 3*TAB + "_" + nombreTabla + "Repository = MEFContainer.Container.GetExport<I" + nombreTabla + "Repository>();" + ENTER
    constructorClase += 2*TAB + "}" + ENTER

    return constructorClase

def generarMetodoCreate(nombreTabla):
    metodoCreate = ""
    nombreVariable = "Id" + nombreTabla

    metodoCreate += 2*TAB + "public int Create" + nombreTabla + "(" + nombreTabla + "Entity " + nombreTabla + ")" + ENTER
    metodoCreate += 2*TAB + "{" + ENTER 
    metodoCreate += 3*TAB + "int " + nombreVariable + " = 0;" + ENTER 
    metodoCreate += 3*TAB + "bool exito = false;" + ENTER 
    metodoCreate += 3*TAB + "using (TransactionScope tx = new TransactionScope())" + ENTER 
    metodoCreate += 3*TAB + "{" + ENTER 
    metodoCreate += 4*TAB + nombreVariable + " = _" + nombreTabla + "Repository.Insert" + nombreTabla + "(" + nombreTabla + ");" + ENTER 
    metodoCreate += 4*TAB + "exito = true;" + ENTER 
    metodoCreate += 4*TAB + "if (exito) tx.Complete();" + ENTER 
    metodoCreate += 3*TAB + "}" + ENTER 
    metodoCreate += 3*TAB + "return " + nombreVariable + ";" + ENTER 
    metodoCreate += 2*TAB + "}" + ENTER

    return metodoCreate

def generarMetodoEdit(nombreTabla):
    metodoEdit = ""
    metodoEdit += 2*TAB + "public bool Edit" + nombreTabla + "(" + nombreTabla + "Entity " + nombreTabla + ")" + ENTER
    metodoEdit += 2*TAB + "{" + ENTER 
    metodoEdit += 3*TAB + "bool exito = false;" + ENTER 
    metodoEdit += 3*TAB + "using (TransactionScope tx = new TransactionScope())" + ENTER 
    metodoEdit += 3*TAB + "{" + ENTER 
    metodoEdit += 4*TAB + "exito = _" + nombreTabla + "Repository.Update" + nombreTabla + "(" + nombreTabla + ");" + ENTER 
    metodoEdit += 4*TAB + "if (exito) tx.Complete();" + ENTER 
    metodoEdit += 3*TAB + "}" + ENTER 
    metodoEdit += 3*TAB + "return exito;" + ENTER 
    metodoEdit += 2*TAB + "}" + ENTER

    return metodoEdit

def generarMetodoDelete(nombreTabla):
    metodoDelete = ""
    tipoDatoClavePrincipal = ""
    clavePrincipal = ""
    tipoDato = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
        clavePrincipal = df["nombreCampo"][i]

    metodoDelete += 2*TAB + "public bool Delete" + nombreTabla + "(" + tipoDatoClavePrincipal + " " + clavePrincipal + ")" + ENTER
    metodoDelete += 2*TAB + "{" + ENTER 
    metodoDelete += 3*TAB + "bool exito = false;" + ENTER 
    metodoDelete += 3*TAB + "exito = _" + nombreTabla + "Repository.Delete" + nombreTabla + "("+ clavePrincipal +");" + ENTER 
    metodoDelete += 3*TAB + "return exito;" + ENTER 
    metodoDelete += 2*TAB + "}" + ENTER

    return metodoDelete

def generarMetodoObtenerByID(nombreTabla):
    metodoObtenerByID = ""
    tipoDatoClavePrincipal = ""
    nombreCampoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
        nombreCampoClavePrincipal = df["nombreCampo"][i]
    
    metodoObtenerByID += 2*TAB + "public " + nombreTabla + "Entity GetById(" + tipoDatoClavePrincipal + " " + nombreCampoClavePrincipal + ")" + ENTER
    metodoObtenerByID += 2*TAB + "{" + ENTER 
    metodoObtenerByID += 3*TAB + nombreTabla + "Entity " + nombreTabla + " = null;" + ENTER 
    metodoObtenerByID += 3*TAB + nombreTabla + " = _" + nombreTabla + "Repository.GetItem" + nombreTabla + "(new " + nombreTabla + "Filter() { " + nombreCampoClavePrincipal + " =  " + nombreCampoClavePrincipal + " }, " + nombreTabla + "FilterItemType.ById);" + ENTER 
    metodoObtenerByID += 3*TAB + "return "+ nombreTabla +";" + ENTER 
    metodoObtenerByID += 2*TAB + "}" + ENTER

    return metodoObtenerByID

def generarMetodoObtenerByPagination(nombreTabla):
    MetodoObtenerByPagination = ""
    MetodoObtenerByPagination += 2*TAB + "public IEnumerable<" + nombreTabla + "Entity> GetByPagination(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterLstItemType filterType, Pagination pagination)" + ENTER
    MetodoObtenerByPagination += 2*TAB + "{" + ENTER 
    MetodoObtenerByPagination += 3*TAB + "List<" + nombreTabla + "Entity> lst = null;" + ENTER 
    MetodoObtenerByPagination += 3*TAB + "lst = _" + nombreTabla + "Repository.GetLstItem" + nombreTabla + "(filter, filterType, pagination).ToList();" + ENTER 
    MetodoObtenerByPagination += 3*TAB + "return lst;" + ENTER 
    MetodoObtenerByPagination += 2*TAB + "}" + ENTER

    return MetodoObtenerByPagination

