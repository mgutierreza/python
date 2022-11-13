from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from objConexionBD.consultasBD import obtenerData
from util.utilitario import gestionArchivos

class objetoRepository(iObjetoAplicacion):

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreClase = ''
        self.TAB = '\t'
        self.ENTER = '\n'
        self.ESPACIO = ' '

    def generarArchivo(self):
        nuevoArchivo = gestionArchivos(self.__nombreTabla, self.__claseObjeto)
        self.__nombreClase = nuevoArchivo.generarNombreArchivo()
        contenidoClase = self.__generarClase()
        nuevoArchivo.generarArchivo(contenidoClase)
        return

    def __generarClase(self):
        clase = ""
        clase += self.__generarCabeceraClase()
        clase += "namespace EP_AcademicMicroservice.Infraestructure" + self.ENTER 
        clase += "{" + self.ENTER
        clase += self.TAB + "[Export(typeof(I" + self.__nombreClase + "))]" + self.ENTER
        clase += self.TAB + "public class " + self.__nombreClase + " : BaseRepository, I" + self.__nombreTabla + "Repository" + self.ENTER
        clase += self.TAB + "{" + self.ENTER         
        clase += self.__generarCuerpoClase()
        clase += self.TAB + "}" + self.ENTER
        clase += "}" + self.ENTER
        return clase
 
    def __generarCabeceraClase(self):
        cabeceraClase = ""
        cabeceraClase += "using System;" + self.ENTER 
        cabeceraClase += "using Dapper;" + self.ENTER 
        cabeceraClase += "using System.Collections.Generic;" + self.ENTER
        cabeceraClase += "using System.Linq;" + self.ENTER 
        cabeceraClase += "using System.Text;" + self.ENTER
        cabeceraClase += "using System.Data;" + self.ENTER
        cabeceraClase += "using System.Composition;" + self.ENTER
        cabeceraClase += "using System.Threading.Tasks;" + self.ENTER
        cabeceraClase += "using EP_AcademicMicroservice.Repository;" + self.ENTER
        cabeceraClase += "using EP_AcademicMicroservice.Entities;" + 2*self.ENTER
        return cabeceraClase

    def __generarCuerpoClase(self):
        cuerpoClase = ""

        cuerpoClase += self.__generarConstructorClase() + self.ENTER 
        cuerpoClase += 2*self.TAB + "#region Public Methods" + self.ENTER 
        cuerpoClase += self.__generarMetodoInsertar() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoActualizar() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoBorrar() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoObtenerItem() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoObtenerLstItem() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodosNoImplementados() + self.ENTER 
        cuerpoClase += 2*self.TAB + "#endregion" + 2*self.ENTER 
        cuerpoClase += 2*self.TAB + "#region Private Methods Item" + self.ENTER     
        cuerpoClase += self.__generarMetodoObtenerByID() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodosObtenerByPagination() + self.ENTER 
        cuerpoClase += 2*self.TAB + "#endregion" + self.ENTER 
        

        return cuerpoClase

    def __generarConstructorClase(self):
        constructorClase = ""

        constructorClase += 2*self.TAB + "#region Constructor" + self.ENTER
        constructorClase += 2*self.TAB + "[ImportingConstructor]" + self.ENTER
        constructorClase += 2*self.TAB + "public " + self.__nombreClase +"(IConnectionFactory cn) : base(cn)" + self.ENTER
        constructorClase += 2*self.TAB + "{" + 2*self.ENTER
        constructorClase += 2*self.TAB + "}" + self.ENTER
        constructorClase += 2*self.TAB + "#endregion" + self.ENTER
        
        return constructorClase
    
    def __generarMetodoInsertar(self):
        metodoInsertar = ""

        metodoInsertar += 2*self.TAB + "public int Insert" + self.__nombreTabla + "(" + self.__nombreTabla + "Entity item)" + self.ENTER
        metodoInsertar += 2*self.TAB + "{" + self.ENTER 
        metodoInsertar += 3*self.TAB + "int afect = 0;" + self.ENTER 
        metodoInsertar += 3*self.TAB + "int Resultado = 0;" + self.ENTER 
        metodoInsertar += 3*self.TAB + "var query = \"" + self.__nombreTabla + "_Insert\";" + self.ENTER 
        metodoInsertar += 3*self.TAB + "var param = new DynamicParameters();" + 2*self.ENTER 
        metodoInsertar += self.__generarCuerpoMetodoInsertar()
        metodoInsertar += 2*self.TAB + "}" + self.ENTER 

        return metodoInsertar    

    def __generarMetodoActualizar(self):
        metodoActualizar = ""
        metodoActualizar += 2*self.TAB + "public bool Update" + self.__nombreTabla + "(" + self.__nombreTabla + "Entity item)" + self.ENTER
        metodoActualizar += 2*self.TAB + "{" + self.ENTER 
        metodoActualizar += 3*self.TAB + "bool result = true;" + self.ENTER 
        metodoActualizar += 3*self.TAB + "int afect = 0;" + self.ENTER 
        metodoActualizar += 3*self.TAB + "var query = \"" + self.__nombreTabla + "_Update\";" + self.ENTER 
        metodoActualizar += 3*self.TAB + "var param = new DynamicParameters();" + 2*self.ENTER 
        metodoActualizar += self.__generarCuerpoMetodoActualizar()
        metodoActualizar += 2*self.TAB + "}" + self.ENTER 

        return metodoActualizar
    
    def __generarMetodoBorrar(self):
        metodoBorrar = ""
        parametros = ""
        variables = ""
        
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()
        for valor in dictData:
            parametros += valor["tipoDatoNET"] + self.ESPACIO + valor["nombreCampo"] + ","
            variables +=  3*self.TAB + "param.Add(\"@" + valor["nombreCampo"] + "\", " + valor["nombreCampo"] + ", DbType." + valor["tipoDatoNET"] + ");" + self.ENTER

        parametros = gestionArchivos.extraerUltimoCaracter(parametros)

        metodoBorrar += 2*self.TAB + "public bool DeleteAcd_MatCursos(" + parametros + ")" + self.ENTER
        metodoBorrar += 2*self.TAB + "{" + self.ENTER
        metodoBorrar += 3*self.TAB + "bool exito = false;" + self.ENTER
        metodoBorrar += 3*self.TAB + "var afect = 0;" + self.ENTER
        metodoBorrar += 3*self.TAB + "var query = \"" + self.__nombreClase + "_Delete\";" + self.ENTER
        metodoBorrar += 3*self.TAB + "var param = new DynamicParameters();" + 2*self.ENTER
        metodoBorrar += variables
        metodoBorrar += 3*self.TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + self.ENTER
        metodoBorrar += 3*self.TAB + "exito = afect > 0;" + 2*self.ENTER
        metodoBorrar += 3*self.TAB + "return exito;" + self.ENTER
        metodoBorrar += 2*self.TAB + "}" + self.ENTER

        return metodoBorrar

    def __generarMetodoObtenerItem(self):
        metodoObtenerItem = ""
        filtro = ""
        
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            filtro += "filter." + valor["nombreCampo"] + ","
        
        filtro = gestionArchivos.extraerUltimoCaracter(filtro)
        
        metodoObtenerItem += 2*self.TAB + "public " + self.__nombreTabla + "Entity GetItem" + self.__nombreTabla + "(" + self.__nombreTabla + "Filter filter, " + self.__nombreTabla + "FilterItemType filterType)" + self.ENTER
        metodoObtenerItem += 2*self.TAB + "{" + self.ENTER
        metodoObtenerItem += 3*self.TAB + self.__nombreTabla + "Entity ItemFound = null;" + self.ENTER
        metodoObtenerItem += 3*self.TAB + "switch (filterType)" + self.ENTER
        metodoObtenerItem += 3*self.TAB + "{" + self.ENTER
        metodoObtenerItem += 4*self.TAB + "case " + self.__nombreTabla + "FilterItemType.ById:" + self.ENTER
        metodoObtenerItem += 5*self.TAB + "ItemFound = this.GetById(" + filtro + ");" + self.ENTER
        metodoObtenerItem += 5*self.TAB + "break;" + self.ENTER
        metodoObtenerItem += 3*self.TAB + "}" + self.ENTER
        metodoObtenerItem += 3*self.TAB + "return ItemFound;" + self.ENTER
        metodoObtenerItem += 2*self.TAB + "}" + self.ENTER

        return metodoObtenerItem

    def __generarMetodoObtenerLstItem(self): 
        campoObtenerLstItem = ""
        filtro = ""
        
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            filtro += "filter." + valor["nombreCampo"] + ","
        
        filtro = gestionArchivos.extraerUltimoCaracter(filtro)        

        campoObtenerLstItem += 2*self.TAB + "public IEnumerable<" + self.__nombreTabla + "Entity> GetLstItem" + self.__nombreTabla + "(" + self.__nombreTabla + "Filter filter, " + self.__nombreTabla + "FilterLstItemType filterType, Pagination pagination)" + self.ENTER
        campoObtenerLstItem += 2*self.TAB + "{" + self.ENTER
        campoObtenerLstItem += 3*self.TAB + "IEnumerable<" + self.__nombreTabla + "Entity> lstItemFound = new List<" + self.__nombreTabla + "Entity>();" + self.ENTER
        campoObtenerLstItem += 3*self.TAB + "switch (filterType)" + self.ENTER
        campoObtenerLstItem += 3*self.TAB + "{" + self.ENTER
        campoObtenerLstItem += 4*self.TAB + "case " + self.__nombreTabla + "FilterLstItemType.ByPagination:" + self.ENTER
        campoObtenerLstItem += 5*self.TAB + "lstItemFound = this.GetByPagination(" + filtro + ");" + self.ENTER
        campoObtenerLstItem += 5*self.TAB + "break;" + self.ENTER
        campoObtenerLstItem += 4*self.TAB + "default: " + self.ENTER
        campoObtenerLstItem += 5*self.TAB + "break;" + self.ENTER        
        campoObtenerLstItem += 3*self.TAB + "}" + self.ENTER
        campoObtenerLstItem += 3*self.TAB + "return lstItemFound;" + self.ENTER
        campoObtenerLstItem += 2*self.TAB + "}" + self.ENTER

        return campoObtenerLstItem

    def __generarMetodosNoImplementados(self):
        metodosNoImplementados = ""

        metodosNoImplementados += 2*self.TAB + "public bool Update(" + self.__nombreTabla + "Entity item)" + self.ENTER
        metodosNoImplementados += 2*self.TAB + "{" + self.ENTER 
        metodosNoImplementados += 3*self.TAB + "throw new NotImplementedException();" + self.ENTER 
        metodosNoImplementados += 2*self.TAB + "}" + 2*self.ENTER 

        metodosNoImplementados += 2*self.TAB + "public bool Delete(long id)" + self.ENTER
        metodosNoImplementados += 2*self.TAB + "{" + self.ENTER 
        metodosNoImplementados += 3*self.TAB + "throw new NotImplementedException();" + self.ENTER 
        metodosNoImplementados += 2*self.TAB + "}" + 2*self.ENTER 

        metodosNoImplementados += 2*self.TAB + "public bool Delete(int id)" + self.ENTER
        metodosNoImplementados += 2*self.TAB + "{" + self.ENTER 
        metodosNoImplementados += 3*self.TAB + "throw new NotImplementedException();" + self.ENTER 
        metodosNoImplementados += 2*self.TAB + "}" + 2*self.ENTER 

        metodosNoImplementados += 2*self.TAB + "public bool Delete(string id)" + self.ENTER
        metodosNoImplementados += 2*self.TAB + "{" + self.ENTER 
        metodosNoImplementados += 3*self.TAB + "throw new NotImplementedException();" + self.ENTER 
        metodosNoImplementados += 2*self.TAB + "}" + 2*self.ENTER 

        return metodosNoImplementados

    def __generarMetodoObtenerByID(self):
        metodoObtenerByID = ""
        parametrosEntrada = ""
        variables = ""
        
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            parametrosEntrada += valor["tipoDatoNET"] + self.ESPACIO + valor["nombreCampo"] + ","
            variables +=  3*self.TAB + "param.Add(\"@" + valor["nombreCampo"] + "\", " + valor["nombreCampo"] + ", DbType." + valor["tipoDatoNET"] + ");" + self.ENTER
        
        parametrosEntrada = gestionArchivos.extraerUltimoCaracter(parametrosEntrada) 

        metodoObtenerByID += 2*self.TAB + "private " + self.__nombreTabla + "Entity GetById(" + parametrosEntrada + ")" + self.ENTER
        metodoObtenerByID += 2*self.TAB + "{" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + self.__nombreTabla + "Entity itemFound = null;" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + "var query =\"" + self.__nombreTabla + "_Get\";" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + "var param = new DynamicParameters();" + self.ENTER 
        metodoObtenerByID += variables
        metodoObtenerByID += 3*self.TAB + "itemFound = SqlMapper.QueryFirstOrDefault<" + self.__nombreTabla + "Entity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*self.ENTER 
        metodoObtenerByID += 3*self.TAB + "return itemFound;" + self.ENTER 
        metodoObtenerByID += 2*self.TAB + "}" + self.ENTER 

        return metodoObtenerByID

    def __generarMetodosObtenerByPagination(self):
        metodoObtenerByPagination = ""
        parametrosEntrada = ""
        variables = ""
        
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            parametrosEntrada += valor["tipoDatoNET"] + self.ESPACIO + valor["nombreCampo"] + ","
            variables +=  3*self.TAB + "param.Add(\"@" + valor["nombreCampo"] + "\", " + valor["nombreCampo"] + ", DbType." + valor["tipoDatoNET"] + ");" + self.ENTER
        
        parametrosEntrada = gestionArchivos.extraerUltimoCaracter(parametrosEntrada) 

        metodoObtenerByPagination += 2*self.TAB + "private IEnumerable<" + self.__nombreTabla + "Entity> GetByPagination(" + parametrosEntrada + ")" + self.ENTER
        metodoObtenerByPagination += 2*self.TAB + "{" + self.ENTER 
        metodoObtenerByPagination += 3*self.TAB + "IEnumerable<" + self.__nombreTabla + "Entity> lstFound = new List<" + self.__nombreTabla + "Entity>();" + self.ENTER 
        metodoObtenerByPagination += 3*self.TAB + "var query =\"" + self.__nombreTabla + "_Get\";" + self.ENTER 
        metodoObtenerByPagination += 3*self.TAB + "var param = new DynamicParameters();" + self.ENTER 
        metodoObtenerByPagination += variables
        metodoObtenerByPagination += 3*self.TAB + "lstFound = SqlMapper.Query<" + self.__nombreTabla + "Entity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*self.ENTER 
        metodoObtenerByPagination += 3*self.TAB + "return lstFound;" + self.ENTER 
        metodoObtenerByPagination += 2*self.TAB + "}" + self.ENTER                   

        return metodoObtenerByPagination

    def __generarCuerpoMetodoInsertar(self):
        campoInsertar = ""
        dictData = {}
        tipoDato = ""
        campoClavePrincipal = ""
           
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataTodosCampos()

        numeroCampos = len(dictData)
        dictData.pop(numeroCampos - 1)
        dictData.pop(numeroCampos - 2)
        dictData.pop(numeroCampos - 3)
        
        for valor in dictData:
            if (valor["tipoCampo"] == 'PRIMARY KEY'):
                tipoDato = valor["tipoDatoNET"]
                campoClavePrincipal = valor["nombreCampo"]
                campoInsertar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] 
                campoInsertar += ", DbType." + valor["tipoDatoNET"] + ", direction: ParameterDirection.Output); " + self.ENTER
            else:
                campoInsertar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] 
                campoInsertar += ", DbType." + valor["tipoDatoNET"] + "); " + self.ENTER

        campoInsertar += self.ENTER
        campoInsertar += 3*self.TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*self.ENTER
        campoInsertar += 3*self.TAB + "Resultado = param.Get<" + tipoDato + ">(\"@" + campoClavePrincipal + "\");" + 2*self.ENTER
        campoInsertar += 3*self.TAB + "return Resultado;" + self.ENTER

        return campoInsertar

    def __generarCuerpoMetodoActualizar(self):
        campoActualizar = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataTodosCampos()
        numeroCampos = len(dictData)
        x = numeroCampos - 4
        y = numeroCampos - 5
        z = numeroCampos - 6
        dictData.pop(x)
        dictData.pop(y)
        dictData.pop(z)
        
        for valor in dictData:
            campoActualizar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] + ", DbType." + valor["tipoDatoNET"]  + "); " + self.ENTER
        
        campoActualizar += 3*self.TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + self.ENTER
        campoActualizar += 3*self.TAB + "Resultado = afect > 0;" + 2*self.ENTER
        campoActualizar += 3*self.TAB + "errorCode = param.Get<string>(\"@errorCode\"));" + 2*self.ENTER
        campoActualizar += 3*self.TAB + "if (errorCode != null)" + self.ENTER
        campoActualizar += 3*self.TAB + "{" + self.ENTER
        campoActualizar += 4*self.TAB + "throw new Fail" + self.__nombreTabla + "Exception(errorCode);" + self.ENTER
        campoActualizar += 3*self.TAB + "}" + 2*self.ENTER
        campoActualizar += 3*self.TAB + "return Resultado" + self.ENTER
        
        return campoActualizar