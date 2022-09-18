import pyodbc as pyo
import pandas as pd
from os import remove
from consultaDatos import obtenerMetaDataClavePrincipal

TAB = "\t"
ENTER = "\n"

def generarArchivoDomain(nombreTabla):
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
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Repository;" + ENTER 
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase = cabeceraClase + "using System;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Composition;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Transactions;" + ENTER
    cabeceraClase = cabeceraClase + "using Util;" + 2*ENTER
    return cabeceraClase

def generarClaseService(nombreTabla):
    claseEntity = ""
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Domain" + ENTER + "{"  + ENTER   
    pieClaseEntity = "}"
    cuerpoClaseEntity = generarCuerpoClaseDomain(nombreTabla)    
    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseDomain(nombreTabla):
    cuerpoClase = ""
    cuerpoClase = cuerpoClase + TAB + "public class " + generarNombreClase(nombreTabla) + ENTER
    cuerpoClase = cuerpoClase + TAB + "{" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region MEF" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "[Import]" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "private I" + nombreTabla + "Repository _" + nombreTabla + "Repository { get; set; }" + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region Constructor" + 2*ENTER 
    cuerpoClase = cuerpoClase + generarConstructorClase(nombreTabla) + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region Methods Public" + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoCreate(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoEdit(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoDelete(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoObtenerByID(nombreTabla) + 2*ENTER
    cuerpoClase = cuerpoClase + generarMetodoObtenerByPagination(nombreTabla) + ENTER
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase = cuerpoClase + TAB + "}" + ENTER
    
    return cuerpoClase

def generarConstructorClase(nombreTabla):
    constructorClase = ""
    constructorClase = constructorClase + 2*TAB + "public " + generarNombreClase(nombreTabla) + "()" + ENTER
    constructorClase = constructorClase + 2*TAB + "{" + ENTER
    constructorClase = constructorClase + 3*TAB + "_" + nombreTabla + "Repository = MEFContainer.Container.GetExport<I" + nombreTabla + "Repository>();" + ENTER
    constructorClase = constructorClase + 2*TAB + "}" + ENTER

    return constructorClase

def generarMetodoCreate(nombreTabla):
    metodoCreate = ""
    nombreVariable = "Id" + nombreTabla

    metodoCreate = metodoCreate + 2*TAB + "public int Create" + nombreTabla + "(" + nombreTabla + "Entity " + nombreTabla + ")" + ENTER
    metodoCreate = metodoCreate + 2*TAB + "{" + ENTER 
    metodoCreate = metodoCreate + 3*TAB + "int " + nombreVariable + " = 0;" + ENTER 
    metodoCreate = metodoCreate + 3*TAB + "bool exito = false;" + ENTER 
    metodoCreate = metodoCreate + 3*TAB + "using (TransactionScope tx = new TransactionScope())" + ENTER 
    metodoCreate = metodoCreate + 3*TAB + "{" + ENTER 
    metodoCreate = metodoCreate + 4*TAB + nombreVariable + " = _" + nombreTabla + "Repository.Insert" + nombreTabla + "(" + nombreTabla + ");" + ENTER 
    metodoCreate = metodoCreate + 4*TAB + "exito = true;" + ENTER 
    metodoCreate = metodoCreate + 4*TAB + "if (exito) tx.Complete();" + ENTER 
    metodoCreate = metodoCreate + 3*TAB + "}" + ENTER 
    metodoCreate = metodoCreate + 3*TAB + "return " + nombreVariable + ";" + ENTER 
    metodoCreate = metodoCreate + 2*TAB + "}" + ENTER

    return metodoCreate

def generarMetodoEdit(nombreTabla):
    metodoEdit = ""
    metodoEdit = metodoEdit + 2*TAB + "public bool Edit" + nombreTabla + "(" + nombreTabla + "Entity " + nombreTabla + ")" + ENTER
    metodoEdit = metodoEdit + 2*TAB + "{" + ENTER 
    metodoEdit = metodoEdit + 3*TAB + "bool exito = false;" + ENTER 
    metodoEdit = metodoEdit + 3*TAB + "using (TransactionScope tx = new TransactionScope())" + ENTER 
    metodoEdit = metodoEdit + 3*TAB + "{" + ENTER 
    metodoEdit = metodoEdit + 4*TAB + "exito = _" + nombreTabla + "Repository.Update" + nombreTabla + "(" + nombreTabla + ")" + ENTER 
    metodoEdit = metodoEdit + 4*TAB + "if (exito) tx.Complete();" + ENTER 
    metodoEdit = metodoEdit + 3*TAB + "}" + ENTER 
    metodoEdit = metodoEdit + 3*TAB + "return exito;" + ENTER 
    metodoEdit = metodoEdit + 2*TAB + "}" + ENTER

    return metodoEdit

def generarMetodoDelete(nombreTabla):
    metodoDelete = ""
    tipoDatoClavePrincipal = ""
    tipoDato = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        tipoDatoClavePrincipal = df["tipoDato"][i]
    
    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "Int32"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "String"
    else:
        tipoDato = "DateTime"

    metodoDelete = metodoDelete + 2*TAB + "public bool Delete" + nombreTabla + "(" + tipoDato + " Id)" + ENTER
    metodoDelete = metodoDelete + 2*TAB + "{" + ENTER 
    metodoDelete = metodoDelete + 3*TAB + "bool exito = false;" + ENTER 
    metodoDelete = metodoDelete + 3*TAB + "exito = _" + nombreTabla + "Repository.Delete" + nombreTabla + "(Id);" + ENTER 
    metodoDelete = metodoDelete + 3*TAB + "return exito;" + ENTER 
    metodoDelete = metodoDelete + 2*TAB + "}" + ENTER

    return metodoDelete

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

    metodoObtenerByID = metodoObtenerByID + 2*TAB + "public " + nombreTabla + "Entity GetById(" + tipoDato + " Id)" + ENTER
    metodoObtenerByID = metodoObtenerByID + 2*TAB + "{" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + nombreTabla + "Entity " + nombreTabla + " = null;" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + nombreTabla + " = _" + nombreTabla + "Repository.GetItem" + nombreTabla + "(new " + nombreTabla + "Filter() { " + nombreCampoClavePrincipal + " = Id }, " + nombreTabla + "FilterItemType.ById);" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "return "+ nombreTabla +";" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 2*TAB + "}" + ENTER

    return metodoObtenerByID

def generarMetodoObtenerByPagination(nombreTabla):
    MetodoObtenerByPagination = ""
    MetodoObtenerByPagination = MetodoObtenerByPagination + 2*TAB + "public IEnumerable<" + nombreTabla + "Entity> GetByPagination(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterLstItemType filterType, Pagination pagination)" + ENTER
    MetodoObtenerByPagination = MetodoObtenerByPagination + 2*TAB + "{" + ENTER 
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "List<" + nombreTabla + "Entity> lst = null;" + ENTER 
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "lst = _" + nombreTabla + "Repository.GetLstItem" + nombreTabla + "(filter, filterType, pagination).ToList();" + ENTER 
    MetodoObtenerByPagination = MetodoObtenerByPagination + 3*TAB + "return lst;" + ENTER 
    MetodoObtenerByPagination = MetodoObtenerByPagination + 2*TAB + "}" + ENTER

    return MetodoObtenerByPagination

def generarNombreClase(nombreTabla):
    return nombreTabla + "Domain"

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase