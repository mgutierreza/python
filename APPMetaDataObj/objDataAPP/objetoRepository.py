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
        clase += self.__generarCuerpoClase()
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

        cuerpoClase += self.TAB + "[Export(typeof(I" + self.__nombreClase + "))]" + self.ENTER
        cuerpoClase += self.TAB + "public class " + self.__nombreClase + " : BaseRepository, I" + self.__nombreTabla + "Repository" + self.ENTER
        cuerpoClase += self.TAB + "{" + self.ENTER 
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
        cuerpoClase += self.__generarMetodosObtenerByID() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodosObtenerByPagination() + self.ENTER 
        cuerpoClase += 2*self.TAB + "#endregion" + self.ENTER 
        cuerpoClase += self.TAB + "}" + self.ENTER

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
        campoClavePrincipal = ""
        tipoDatoClavePrincipal = ""
        tipoDato = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            campoClavePrincipal = valor["nombreCampo"]
            tipoDatoClavePrincipal = valor["tipoDato"]

        if (tipoDatoClavePrincipal == 'INT'):
            tipoDato = "int"
        elif (tipoDatoClavePrincipal == 'VARCHAR'):
            tipoDato = "var"
        else:
            tipoDato = "datetime"

        metodoInsertar += 2*self.TAB + "public " + tipoDato + " Insert" + self.__nombreTabla + "(" + self.__nombreTabla + "Entity item)" + self.ENTER
        metodoInsertar += 2*self.TAB + "{" + self.ENTER 
        metodoInsertar += 3*self.TAB + "int afect = 0;" + self.ENTER 
        metodoInsertar += 3*self.TAB + tipoDato + " Resultado = 0;" + self.ENTER 
        metodoInsertar += 3*self.TAB + "var query = \"" + self.__nombreTabla + "_Insert\";" + self.ENTER 
        metodoInsertar += 3*self.TAB + "var param = new DynamicParameters();" + 2*self.ENTER 
        metodoInsertar += self.__generarCamposInsertar() + self.ENTER
        metodoInsertar += 3*self.TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*self.ENTER
        metodoInsertar += 3*self.TAB + "Resultado = param.Get<" + tipoDato + ">(\"@" + campoClavePrincipal + "\");" + 2*self.ENTER
        metodoInsertar += 3*self.TAB + "return Resultado;" + self.ENTER
        metodoInsertar += 2*self.TAB + "}" + self.ENTER 

        return metodoInsertar    

    def __generarCamposInsertar(self):
        campoInsertar = ""
        tipoDato = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataTodosCampos()

        numeroCampos = len(dictData)
        rangoMenor = numeroCampos - 3
        #rangoMayor = numeroCampos

        for i, v in enumerate(dictData):
            if (i >= rangoMenor):
                dictData.pop(i)
        
        for valor in dictData:
            if (valor["tipoDato"] == 'INT'):
                tipoDato = "DbType.Int32"
            elif (valor["tipoDato"] == 'VARCHAR'):
                tipoDato = "DbType.String"
            else:
                tipoDato = "DbType.DateTime"

            if (valor["tipoCampo"] == 'PRIMARY KEY'):
                campoInsertar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] 
                campoInsertar += ", " + tipoDato + ", direction: ParameterDirection.Output); " + self.ENTER
            else:
                campoInsertar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] 
                campoInsertar += ", " + tipoDato + "); " + self.ENTER

        return campoInsertar

    def __generarMetodoActualizar(self):
        metodoActualizar = ""
        metodoActualizar += 2*self.TAB + "public bool Update" + self.__nombreTabla + "(" + self.__nombreTabla + "Entity item)" + self.ENTER
        metodoActualizar += 2*self.TAB + "{" + self.ENTER 
        metodoActualizar += 3*self.TAB + "bool result = true;" + self.ENTER 
        metodoActualizar += 3*self.TAB + "int afect = 0;" + self.ENTER 
        metodoActualizar += 3*self.TAB + "var query = \"" + self.__nombreTabla + "_Update\";" + self.ENTER 
        metodoActualizar += 3*self.TAB + "var param = new DynamicParameters();" + 2*self.ENTER 
        metodoActualizar += self.__generarCamposActualizar() + self.ENTER
        metodoActualizar += 3*self.TAB + "afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);" + 2*self.ENTER
        metodoActualizar += 3*self.TAB + "return result" + self.ENTER
        metodoActualizar += 2*self.TAB + "}" + self.ENTER 

        return metodoActualizar

    def generarCamposActualizar(self):
        campoActualizar = ""
        tipoDato = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataTodosCampos()

        numeroCampos = len(dictData)
        rangoMenor = numeroCampos - 6
        rangoMayor = numeroCampos - 3
        #df = df.drop(range(rangoMenor,rangoMayor))
        for i, v in enumerate(dictData):
            if (i >= rangoMenor and i <= rangoMayor):
                dictData.pop(i)

        for valor in dictData:
            if (valor["tipoDato"] == 'INT'):
                tipoDato = "DbType.Int32"
            elif (valor == 'VARCHAR'):
                tipoDato = "DbType.String"
            else:
                tipoDato = "DbType.DateTime"

            campoActualizar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] + ", " + tipoDato + "); " + self.ENTER

        return campoActualizar