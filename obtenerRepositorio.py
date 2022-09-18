import pyodbc as pyo
import pandas as pd
from os import remove
from consultaDatos import obtenerMetaDataCampos, obtenerMetaDataClavePrincipal

TAB = "\t"
ENTER = "\n"

def generarArchivoRepository(nombreTabla):
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
    cabeceraClaseEntity = "namespace EP_AcademicMicroservice.Infraestructure" + ENTER + "{"  + ENTER   
    pieClaseEntity = "}"

    cuerpoClaseEntity = generarCuerpoClaseRequest(nombreTabla)    

    claseEntity = cabeceraClaseEntity + cuerpoClaseEntity + pieClaseEntity

    return claseEntity

def generarCuerpoClaseRequest(nombreTabla):
    cuerpoClase = ""
    cuerpoClase = cuerpoClase + TAB + "[Export(typeof(I" + nombreTabla + "Repository))]"
    cuerpoClase = cuerpoClase + TAB + "public class " + generarNombreClase(nombreTabla) + " : BaseRepository, I" + nombreTabla + "Repository" + ENTER
    cuerpoClase = cuerpoClase + TAB + "{" + ENTER 
    cuerpoClase = cuerpoClase + generarConstructorClase(nombreTabla) + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region Public Methods" + ENTER 
    cuerpoClase = cuerpoClase + generarMetodoInsertar(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoActualizar(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoBorrar(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoObtenerItem(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodoObtenerLstItem(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodosNoImplementados(nombreTabla) + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#region Private Methods Item" + ENTER     
    cuerpoClase = cuerpoClase + generarMetodosObtenerByID(nombreTabla) + 2*ENTER 
    cuerpoClase = cuerpoClase + generarMetodosObtenerByPagination(nombreTabla) + ENTER 
    cuerpoClase = cuerpoClase + 2*TAB + "#endregion" + ENTER 
    cuerpoClase = cuerpoClase + TAB + "}" + ENTER
    
    return cuerpoClase

def generarMetodosObtenerByPagination(nombreTabla):
    metodoObtenerByPagination = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""
    tipoDato = ""
    
    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDato"][i]
    
    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "DbType.Int32"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "DbType.String"
    else:
        tipoDato = "DbType.DateTime"

    metodoObtenerByPagination = metodoObtenerByPagination + 2*TAB + "private IEnumerable<" + nombreTabla + "Entity> GetByPagination()" + ENTER
    metodoObtenerByPagination = metodoObtenerByPagination + 2*TAB + "{" + ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 3*TAB + "IEnumerable<" + nombreTabla + "Entity> lstFound = new List<" + nombreTabla + "Entity>();" + ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 3*TAB + "var query =\"" + nombreTabla + "_Get\";" + ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 3*TAB + "var param = new DynamicParameters();" + ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 3*TAB + "param.Add(\"@" + campoClavePrincipal + "\", 0, " + tipoDato + ");" + ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 3*TAB + "lstFound = SqlMapper.Query" + nombreTabla + "Entity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 3*TAB + "return lstFound;" + ENTER 
    metodoObtenerByPagination = metodoObtenerByPagination + 2*TAB + "}" + ENTER     
    
    return metodoObtenerByPagination


def generarMetodosObtenerByID(nombreTabla):
    metodoObtenerByID = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""
    tipoDato = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDato"][i]
    
    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "DbType.Int32"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "DbType.String"
    else:
        tipoDato = "DbType.DateTime"

    metodoObtenerByID = metodoObtenerByID + 2*TAB + "private " + nombreTabla + "Entity GetById(" + tipoDato + " Id)" + ENTER
    metodoObtenerByID = metodoObtenerByID + 2*TAB + "{" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + nombreTabla + "Entity itemFound = null;" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "var query =\"" + nombreTabla + "_Get\";" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "var param = new DynamicParameters();" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "param.Add(\"@" + campoClavePrincipal + "\", Id, " + tipoDato + ");" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "itemFound = SqlMapper.QueryFirstOrDefault<" + nombreTabla + "Entity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER 
    metodoObtenerByID = metodoObtenerByID + 3*TAB + "return itemFound;" + ENTER 
    metodoObtenerByID = metodoObtenerByID + 2*TAB + "}" + ENTER 

    return metodoObtenerByID


def generarMetodosNoImplementados(nombreTabla):
    metodosNoImplementados = ""

    metodosNoImplementados = metodosNoImplementados + 2*TAB + "public bool Update(" + nombreTabla + "Entity item)" + ENTER
    metodosNoImplementados = metodosNoImplementados + 2*TAB + "{" + ENTER 
    metodosNoImplementados = metodosNoImplementados + 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados = metodosNoImplementados + 2*TAB + "}" + 2*ENTER 

    metodosNoImplementados = metodosNoImplementados + 2*TAB + "public bool Delete(long id)" + ENTER
    metodosNoImplementados = metodosNoImplementados + 2*TAB + "{" + ENTER 
    metodosNoImplementados = metodosNoImplementados + 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados = metodosNoImplementados + 2*TAB + "}" + 2*ENTER 

    metodosNoImplementados = metodosNoImplementados + 2*TAB + "public bool Delete(string id)" + ENTER
    metodosNoImplementados = metodosNoImplementados + 2*TAB + "{" + ENTER 
    metodosNoImplementados = metodosNoImplementados + 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados = metodosNoImplementados + 2*TAB + "}" + 2*ENTER 

    return metodosNoImplementados

def generarMetodoObtenerLstItem(nombreTabla):
    metodoObtenerLstItem = ""

    metodoObtenerLstItem = metodoObtenerLstItem + 2*TAB + "public IEnumerable<" + nombreTabla + "Entity> GetLstItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterLstItemType filterType, Pagination pagination)" + ENTER
    metodoObtenerLstItem = metodoObtenerLstItem + 2*TAB + "{" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 3*TAB + "IEnumerable<" + nombreTabla + "Entity> lstItemFound = new List<" + nombreTabla + "Entity>();" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 3*TAB + "switch (filterType)" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 3*TAB + "{" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 4*TAB + "case " + nombreTabla + "FilterLstItemType.ByPagination:" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 5*TAB + "lstItemFound = this.GetByPagination();" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 5*TAB + "break;" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 4*TAB + "default:" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 5*TAB + "break;" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 3*TAB + "}" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 3*TAB + "return lstItemFound;" + ENTER 
    metodoObtenerLstItem = metodoObtenerLstItem + 2*TAB + "}" + ENTER 

    return metodoObtenerLstItem


def generarMetodoObtenerItem(nombreTabla):
    metodoObtenerItem = ""
    campoClavePrincipal = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]

    metodoObtenerItem = metodoObtenerItem + 2*TAB + "public " + nombreTabla + "Entity GetItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterItemType filterType)" + ENTER
    metodoObtenerItem = metodoObtenerItem + 2*TAB + "{" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 3*TAB + nombreTabla + "Entity ItemFound = null;" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 3*TAB + "switch (filterType)" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 3*TAB + "{" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 4*TAB + "case " + nombreTabla + "FilterItemType.ById:" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 5*TAB + "ItemFound = this.GetById(filter." + campoClavePrincipal + ");" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 5*TAB + "break;" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 3*TAB + "}" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 3*TAB + "return ItemFound;" + ENTER 
    metodoObtenerItem = metodoObtenerItem + 2*TAB + "}" + ENTER 

    return metodoObtenerItem

def generarMetodoBorrar(nombreTabla):
    metodoBorrar = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""
    tipoDato = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDato"][i]
    
    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "DbType.Int32"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "DbType.String"
    else:
        tipoDato = "DbType.DateTime"

    metodoBorrar = metodoBorrar + 2*TAB + "public bool Delete" + nombreTabla + "(" + tipoDato + " Id)" + ENTER
    metodoBorrar = metodoBorrar + 2*TAB + "{" + ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "bool exito = false;" + ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "var afect = 0;" + ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "var query = \"" + nombreTabla + "_Delete\";" + ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "var param = new DynamicParameters();" + 2*ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "param.Add(\"@" + campoClavePrincipal + "\", Id, " + tipoDato + ");" + ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "exito = afect > 0;" + 2*ENTER 
    metodoBorrar = metodoBorrar + 3*TAB + "return exito" + ENTER 
    metodoBorrar = metodoBorrar + 2*TAB + "}" + ENTER 

    return metodoBorrar

def generarMetodoInsertar(nombreTabla):
    metodoInsertar = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""
    tipoDato = ""

    df = obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDato"][i]

    if (tipoDatoClavePrincipal == 'INT'):
        tipoDato = "int"
    elif (tipoDatoClavePrincipal == 'VARCHAR'):
        tipoDato = "var"
    else:
        tipoDato = "datetime"

    metodoInsertar = metodoInsertar + 2*TAB + "public " + tipoDato + " Insert" + nombreTabla + "(" + nombreTabla + "Entity item)" + ENTER
    metodoInsertar = metodoInsertar + 2*TAB + "{" + ENTER 
    metodoInsertar = metodoInsertar + 3*TAB + "int afect = 0;" + ENTER 
    metodoInsertar = metodoInsertar + 3*TAB + tipoDato + " Resultado = 0;" + ENTER 
    metodoInsertar = metodoInsertar + 3*TAB + "var query = \"" + nombreTabla + "_Insert\";" + ENTER 
    metodoInsertar = metodoInsertar + 3*TAB + "var param = new DynamicParameters();" + 2*ENTER 
    metodoInsertar = metodoInsertar + generarCamposInsertar(nombreTabla) + ENTER
    metodoInsertar = metodoInsertar + 3*TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER
    metodoInsertar = metodoInsertar + 3*TAB + "Resultado = param.Get<" + tipoDato + ">(\"@" + campoClavePrincipal + "\");" + 2*ENTER
    metodoInsertar = metodoInsertar + 3*TAB + "return Resultado;" + ENTER
    metodoInsertar = metodoInsertar + 2*TAB + "}" + ENTER 

    return metodoInsertar

def generarMetodoActualizar(nombreTabla):
    metodoActualizar = ""
    metodoActualizar = metodoActualizar + 2*TAB + "public bool Update" + nombreTabla + "(" + nombreTabla + "Entity item)" + ENTER
    metodoActualizar = metodoActualizar + 2*TAB + "{" + ENTER 
    metodoActualizar = metodoActualizar + 3*TAB + "bool result = true;" + ENTER 
    metodoActualizar = metodoActualizar + 3*TAB + "int afect = 0;" + ENTER 
    metodoActualizar = metodoActualizar + 3*TAB + "var query = \"" + nombreTabla + "_Update\";" + ENTER 
    metodoActualizar = metodoActualizar + 3*TAB + "var param = new DynamicParameters();" + 2*ENTER 
    metodoActualizar = metodoActualizar + generarCamposActualizar(nombreTabla) + ENTER
    metodoActualizar = metodoActualizar + 3*TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER
    metodoActualizar = metodoActualizar + 3*TAB + "return result" + ENTER
    metodoActualizar = metodoActualizar + 2*TAB + "}" + ENTER 

    return metodoActualizar

def generarCamposActualizar(nombreTabla):
    campoActualizar = ""
    tipoDato = ""

    df0 = obtenerMetaDataCampos(nombreTabla)

    numeroCampos = len(df0.index)
    rangoMenor = numeroCampos - 6
    rangoMayor = numeroCampos - 3
    df = df0.drop(range(rangoMenor,rangoMayor))
    numeroCampos = len(df.index)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            tipoDato = "DbType.Int32"
        elif (df["tipoDato"][i] == 'VARCHAR'):
            tipoDato = "DbType.String"
        else:
            tipoDato = "DbType.DateTime"

        if (df["tipoCampo"][i] != 'PRIMARY KEY'):
            campoActualizar = campoActualizar + 3*TAB + "param.Add(@" + df["nombreCampo"][i] + ", item." + df["nombreCampo"][i] + ", " + tipoDato + "); " + ENTER

    return campoActualizar

def generarCamposInsertar(nombreTabla):
    campoInsertar = ""
    tipoDato = ""

    df0 = obtenerMetaDataCampos(nombreTabla)

    numeroCampos = len(df0.index)
    rangoMenor = numeroCampos - 3
    rangoMayor = numeroCampos
    df = df0.drop(range(rangoMenor,rangoMayor))
    numeroCampos = len(df.index)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            tipoDato = "DbType.Int32"
        elif (df["tipoDato"][i] == 'VARCHAR'):
            tipoDato = "DbType.String"
        else:
            tipoDato = "DbType.DateTime"

        if (df["tipoCampo"][i] == 'PRIMARY KEY'):
            campoInsertar = campoInsertar + 3*TAB + "param.Add(@" + df["nombreCampo"][i] + ", item." + df["nombreCampo"][i] + ", " + tipoDato + ", direction: ParameterDirection.Output); " + ENTER
        else:
            campoInsertar = campoInsertar + 3*TAB + "param.Add(@" + df["nombreCampo"][i] + ", item." + df["nombreCampo"][i] + ", " + tipoDato + "); " + ENTER

    return campoInsertar

def generarConstructorClase(nombreTabla):
    constructorClase = ""
    constructorClase = constructorClase + 2*TAB + "#region Constructor" + ENTER
    constructorClase = constructorClase + 2*TAB + "[ImportingConstructor]" + ENTER
    constructorClase = constructorClase + 2*TAB + "public " + nombreTabla + "Repository(IConnectionFactory cn) : base(cn)" + ENTER
    constructorClase = constructorClase + 2*TAB + "{" + 2*ENTER
    constructorClase = constructorClase + 2*TAB + "}" + ENTER
    constructorClase = constructorClase + 2*TAB + "#endregion" + ENTER
    return constructorClase

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase = cabeceraClase + "using Dapper;" + ENTER 
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase = cabeceraClase + "using EP_AcademicMicroservice.Repository;" + ENTER
    cabeceraClase = cabeceraClase + "using System;" + ENTER 
    cabeceraClase = cabeceraClase + "using System.Collections.Generic;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Composition;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Data;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Linq;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Text;" + ENTER
    cabeceraClase = cabeceraClase + "using System.Threading.Tasks;" + ENTER
    return cabeceraClase

def generarNombreClase(nombreTabla):
    return nombreTabla + "Repository"

def generarNombreArchivo(nombreClase):
    nombreClase = nombreClase + ".cs"
    return nombreClase