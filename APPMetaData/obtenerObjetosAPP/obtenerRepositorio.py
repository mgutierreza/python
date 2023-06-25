import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos

TAB = "\t"
ENTER = "\n"

def generarArchivoRepository(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.repository)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace " + getNombreProyecto() + "Microservice.Infraestructure" + ENTER 
    claseEntity += "{"  + ENTER   
    claseEntity += generarCuerpoClase(nombreTabla)
    claseEntity += "}"

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using Dapper;" + ENTER 
    cabeceraClase += "using EP_AcademicMicroservice.Entities;" + ENTER 
    cabeceraClase += "using EP_AcademicMicroservice.Repository;" + ENTER
    cabeceraClase += "using EP_AcademicMicroservice.Exceptions;" + ENTER
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Composition;" + ENTER
    cabeceraClase += "using System.Data;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""
    cuerpoClase += TAB + "[Export(typeof(I" + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.repository) + "))]" + ENTER
    cuerpoClase += TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.repository) + " : BaseRepository, I" + nombreTabla + "Repository" + ENTER
    cuerpoClase += TAB + "{" + ENTER 
    cuerpoClase += generarConstructorClase(nombreTabla) + ENTER 
    cuerpoClase += 2*TAB + "#region Public Methods" + ENTER 
    cuerpoClase += generarMetodoInsertar(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoActualizar(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoBorrar(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoObtenerItem(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodoObtenerLstItem(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodosNoImplementados(nombreTabla) + ENTER 
    cuerpoClase += 2*TAB + "#endregion" + 2*ENTER 
    cuerpoClase += 2*TAB + "#region Private Methods Item" + ENTER     
    cuerpoClase += generarMetodosObtenerByID(nombreTabla) + 2*ENTER 
    cuerpoClase += generarMetodosObtenerByPagination(nombreTabla) + ENTER 
    cuerpoClase += 2*TAB + "#endregion" + ENTER 
    cuerpoClase += TAB + "}" + ENTER
    
    return cuerpoClase

def generarConstructorClase(nombreTabla):
    constructorClase = ""
    constructorClase += 2*TAB + "#region Constructor" + ENTER
    constructorClase += 2*TAB + "[ImportingConstructor]" + ENTER
    constructorClase += 2*TAB + "public " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.repository) +"(IConnectionFactory cn) : base(cn)" + ENTER
    constructorClase += 2*TAB + "{" + 2*ENTER
    constructorClase += 2*TAB + "}" + ENTER
    constructorClase += 2*TAB + "#endregion" + ENTER
    return constructorClase

def generarMetodoInsertar(nombreTabla):
    metodoInsertar = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]

    metodoInsertar += 2*TAB + "public int Insert" + nombreTabla + "(" + nombreTabla + "Entity item)" + ENTER
    metodoInsertar += 2*TAB + "{" + ENTER 
    metodoInsertar += 3*TAB + "int afect = 0;" + ENTER 
    metodoInsertar += 3*TAB + tipoDatoClavePrincipal + " Resultado = 0;" + ENTER 
    metodoInsertar += 3*TAB + "var query = \"" + nombreTabla + "_Insert\";" + ENTER 
    metodoInsertar += 3*TAB + "var param = new DynamicParameters();" + 2*ENTER 
    metodoInsertar += generarCamposInsertar(nombreTabla) + ENTER
    metodoInsertar += 3*TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER
    metodoInsertar += 3*TAB + "Resultado = param.Get<" + tipoDatoClavePrincipal + ">(\"@" + campoClavePrincipal + "\");" + 2*ENTER
    metodoInsertar += 3*TAB + "return (int)Resultado;" + ENTER
    metodoInsertar += 2*TAB + "}" + ENTER 

    return metodoInsertar

def generarMetodoActualizar(nombreTabla):
    metodoActualizar = ""
    metodoActualizar += 2*TAB + "public bool Update" + nombreTabla + "(" + nombreTabla + "Entity item)" + ENTER
    metodoActualizar += 2*TAB + "{" + ENTER 
    metodoActualizar += 3*TAB + "bool Resultado = true;" + ENTER 
    metodoActualizar += 3*TAB + "int afect = 0;" + ENTER 
    metodoActualizar += 3*TAB + "string errorCode;" + ENTER 
    metodoActualizar += 3*TAB + "var query = \"" + nombreTabla + "_Update\";" + ENTER 
    metodoActualizar += 3*TAB + "var param = new DynamicParameters();" + 2*ENTER 
    metodoActualizar += generarCamposActualizar(nombreTabla) + ENTER
    metodoActualizar += 3*TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + ENTER
    metodoActualizar += 3*TAB + "Resultado = afect > 0;" + 2*ENTER
    metodoActualizar += 3*TAB + "errorCode = param.Get<string>(\"@errorCode\");" + 2*ENTER
    metodoActualizar += 3*TAB + "if (errorCode != null)" + ENTER
    metodoActualizar += 3*TAB + "{" + ENTER
    metodoActualizar += 4*TAB + "throw new " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.exception) + "(errorCode);" + ENTER
    metodoActualizar += 3*TAB + "}" + ENTER
    metodoActualizar += 3*TAB + "return Resultado;" + ENTER
    metodoActualizar += 2*TAB + "}" + ENTER 

    return metodoActualizar

def generarMetodoBorrar(nombreTabla):
    metodoBorrar = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
    
    metodoBorrar += 2*TAB + "public bool Delete" + nombreTabla + "(" + tipoDatoClavePrincipal + " " + campoClavePrincipal + ")" + ENTER
    metodoBorrar += 2*TAB + "{" + ENTER 
    metodoBorrar += 3*TAB + "bool exito = false;" + ENTER 
    metodoBorrar += 3*TAB + "var afect = 0;" + ENTER 
    metodoBorrar += 3*TAB + "var query = \"" + nombreTabla + "_Delete\";" + ENTER 
    metodoBorrar += 3*TAB + "var param = new DynamicParameters();" + 2*ENTER 
    metodoBorrar += 3*TAB + "param.Add(\"@" + campoClavePrincipal + "\", " + campoClavePrincipal + ", DbType." + tipoDatoClavePrincipal + ");" + ENTER 
    metodoBorrar += 3*TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + ENTER 
    metodoBorrar += 3*TAB + "exito = afect > 0;" + 2*ENTER 
    metodoBorrar += 3*TAB + "return exito;" + ENTER 
    metodoBorrar += 2*TAB + "}" + ENTER 

    return metodoBorrar

def generarMetodoObtenerItem(nombreTabla):
    metodoObtenerItem = ""
    campoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]

    metodoObtenerItem += 2*TAB + "public " + nombreTabla + "Entity GetItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterItemType filterType)" + ENTER
    metodoObtenerItem += 2*TAB + "{" + ENTER 
    metodoObtenerItem += 3*TAB + nombreTabla + "Entity ItemFound = null;" + ENTER 
    metodoObtenerItem += 3*TAB + "switch (filterType)" + ENTER 
    metodoObtenerItem += 3*TAB + "{" + ENTER 
    metodoObtenerItem += 4*TAB + "case " + nombreTabla + "FilterItemType.ById:" + ENTER 
    metodoObtenerItem += 5*TAB + "ItemFound = this.GetById(filter." + campoClavePrincipal + ");" + ENTER 
    metodoObtenerItem += 5*TAB + "break;" + ENTER 
    metodoObtenerItem += 3*TAB + "}" + ENTER 
    metodoObtenerItem += 3*TAB + "return ItemFound;" + ENTER 
    metodoObtenerItem += 2*TAB + "}" + ENTER 

    return metodoObtenerItem

def generarMetodoObtenerLstItem(nombreTabla):
    metodoObtenerLstItem = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]

    metodoObtenerLstItem += 2*TAB + "public IEnumerable<" + nombreTabla + "Entity> GetLstItem" + nombreTabla + "(" + nombreTabla + "Filter filter, " + nombreTabla + "FilterLstItemType filterType, Pagination pagination)" + ENTER
    metodoObtenerLstItem += 2*TAB + "{" + ENTER 
    metodoObtenerLstItem += 3*TAB + "IEnumerable<" + nombreTabla + "Entity> lstItemFound = new List<" + nombreTabla + "Entity>();" + ENTER 
    metodoObtenerLstItem += 3*TAB + "switch (filterType)" + ENTER 
    metodoObtenerLstItem += 3*TAB + "{" + ENTER 
    metodoObtenerLstItem += 4*TAB + "case " + nombreTabla + "FilterLstItemType.ByPagination:" + ENTER 
    metodoObtenerLstItem += 5*TAB + "lstItemFound = this.GetByPagination(filter." + campoClavePrincipal +");" + ENTER 
    metodoObtenerLstItem += 5*TAB + "break;" + ENTER 
    metodoObtenerLstItem += 4*TAB + "default:" + ENTER 
    metodoObtenerLstItem += 5*TAB + "break;" + ENTER 
    metodoObtenerLstItem += 3*TAB + "}" + ENTER 
    metodoObtenerLstItem += 3*TAB + "return lstItemFound;" + ENTER 
    metodoObtenerLstItem += 2*TAB + "}" + ENTER 

    return metodoObtenerLstItem

def generarMetodosNoImplementados(nombreTabla):
    metodosNoImplementados = ""

    metodosNoImplementados += 2*TAB + "public bool Update(" + nombreTabla + "Entity item)" + ENTER
    metodosNoImplementados += 2*TAB + "{" + ENTER 
    metodosNoImplementados += 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados += 2*TAB + "}" + 2*ENTER 

    metodosNoImplementados += 2*TAB + "public bool Delete(long id)" + ENTER
    metodosNoImplementados += 2*TAB + "{" + ENTER 
    metodosNoImplementados += 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados += 2*TAB + "}" + 2*ENTER 

    metodosNoImplementados += 2*TAB + "public bool Delete(int id)" + ENTER
    metodosNoImplementados += 2*TAB + "{" + ENTER 
    metodosNoImplementados += 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados += 2*TAB + "}" + 2*ENTER 

    metodosNoImplementados += 2*TAB + "public bool Delete(string id)" + ENTER
    metodosNoImplementados += 2*TAB + "{" + ENTER 
    metodosNoImplementados += 3*TAB + "throw new NotImplementedException();" + ENTER 
    metodosNoImplementados += 2*TAB + "}" + 2*ENTER 

    return metodosNoImplementados

def generarMetodosObtenerByID(nombreTabla):
    metodoObtenerByID = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]
    
    metodoObtenerByID += 2*TAB + "private " + nombreTabla + "Entity GetById(" + tipoDatoClavePrincipal + " " + campoClavePrincipal + ")" + ENTER
    metodoObtenerByID += 2*TAB + "{" + ENTER 
    metodoObtenerByID += 3*TAB + nombreTabla + "Entity itemFound = null;" + ENTER 
    metodoObtenerByID += 3*TAB + "var query =\"" + nombreTabla + "_Get\";" + ENTER 
    metodoObtenerByID += 3*TAB + "var param = new DynamicParameters();" + ENTER 
    metodoObtenerByID += 3*TAB + "param.Add(\"@" + campoClavePrincipal + "\", " + campoClavePrincipal + ", DbType." + tipoDatoClavePrincipal + ");" + ENTER 
    metodoObtenerByID += 3*TAB + "itemFound = SqlMapper.QueryFirstOrDefault<" + nombreTabla + "Entity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER 
    metodoObtenerByID += 3*TAB + "return itemFound;" + ENTER 
    metodoObtenerByID += 2*TAB + "}" + ENTER 

    return metodoObtenerByID

def generarMetodosObtenerByPagination(nombreTabla):
    metodoObtenerByPagination = ""
    campoClavePrincipal = ""
    tipoDatoClavePrincipal = ""
   
    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    for i in df.index:
        campoClavePrincipal = df["nombreCampo"][i]
        tipoDatoClavePrincipal = df["tipoDatoNET"][i]

    metodoObtenerByPagination += 2*TAB + "private IEnumerable<" + nombreTabla + "Entity> GetByPagination(" + tipoDatoClavePrincipal + " " + campoClavePrincipal + ")" + ENTER
    metodoObtenerByPagination += 2*TAB + "{" + ENTER 
    metodoObtenerByPagination += 3*TAB + "IEnumerable<" + nombreTabla + "Entity> lstFound = new List<" + nombreTabla + "Entity>();" + ENTER 
    metodoObtenerByPagination += 3*TAB + "var query =\"" + nombreTabla + "_Get\";" + ENTER 
    metodoObtenerByPagination += 3*TAB + "var param = new DynamicParameters();" + ENTER 
    metodoObtenerByPagination += 3*TAB + "param.Add(\"@" + campoClavePrincipal + "\", " + campoClavePrincipal + ", DbType." + tipoDatoClavePrincipal + ");" + ENTER 
    metodoObtenerByPagination += 3*TAB + "lstFound = SqlMapper.Query<" + nombreTabla + "Entity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*ENTER 
    metodoObtenerByPagination += 3*TAB + "return lstFound;" + ENTER 
    metodoObtenerByPagination += 2*TAB + "}" + ENTER     
    
    return metodoObtenerByPagination

def generarCamposInsertar(nombreTabla):
    campoInsertar = ""
    tipoDato = ""

    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)

    numeroCampos = len(df.index)
    rangoMenor = numeroCampos - 3
    rangoMayor = numeroCampos
    #df = df.drop(range(rangoMenor,rangoMayor))
    
    for i in df.index:
        tipoDato = df["tipoDatoNET"][i]
        if (df["tipoCampo"][i] == 'PRIMARY KEY'):
            campoInsertar += 3*TAB + "param.Add(\"@" + df["nombreCampo"][i] + "\", item." + df["nombreCampo"][i] 
            campoInsertar += ", DbType." + tipoDato + ", direction: ParameterDirection.Output); " + ENTER
        else:
            if((df["tipoCampo"][i] == 'CAMPO') and (df["tipoDatoBD"][i] == 'DATETIME') and ('Registro' in df["nombreCampo"][i])):
                campoInsertar += ""
            else:
                campoInsertar += 3*TAB + "param.Add(\"@" + df["nombreCampo"][i] + "\", item." + df["nombreCampo"][i] 
                campoInsertar += ", DbType." + tipoDato + "); " + ENTER

    return campoInsertar

def generarCamposActualizar(nombreTabla):
    campoActualizar = ""
    tipoDato = ""

    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)

    numeroCampos = len(df.index)

    if(numeroCampos > 3):
        rangoMenor = numeroCampos - 6
        rangoMayor = numeroCampos - 3
        #df = df.drop(range(rangoMenor,rangoMayor))
    
    for i in df.index:
        tipoDato = df["tipoDatoNET"][i]
        if((df["tipoCampo"][i] == 'CAMPO') and (df["tipoDatoBD"][i] == 'DATETIME') and ('Upd' in df["nombreCampo"][i])):
            campoActualizar += ""
        else:
            campoActualizar += 3*TAB + "param.Add(\"@" + df["nombreCampo"][i] + "\", item." + df["nombreCampo"][i] + ", DbType." + tipoDato + "); " + ENTER
        
    campoActualizar +="param.Add(\"@errorCode\", \"\", DbType.String, direction: ParameterDirection.Output);" + ENTER

    return campoActualizar


