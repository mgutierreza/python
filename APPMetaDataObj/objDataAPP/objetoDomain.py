from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from util.utilitario import gestionArchivos
from objConexionBD.consultasBD import obtenerData

class objetoResponse(iObjetoAplicacion):

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
        clase += "namespace EP_AcademicMicroservice.Domain" + self.ENTER 
        clase += "{"  + self.ENTER    
        clase += self.TAB + "public class " + self.__nombreClase + self.ENTER
        clase += self.TAB + "{" + self.ENTER         
        clase += self.__generarCuerpoClase()
        clase += self.TAB + "}" + self.ENTER
        clase += "}"

        return clase

    def __generarCabeceraClase(self):
        cabeceraClase = ""
        cabeceraClase += "using EP_AcademicMicroservice.Repository;" + self.ENTER  
        cabeceraClase += "using EP_AcademicMicroservice.Entities;" + self.ENTER  
        cabeceraClase += "using System;" + self.ENTER  
        cabeceraClase += "using System.Collections.Generic;" + self.ENTER 
        cabeceraClase += "using System.Composition;" + self.ENTER 
        cabeceraClase += "using System.Linq;" + self.ENTER 
        cabeceraClase += "using System.Text;" + self.ENTER 
        cabeceraClase += "using System.Threading.Tasks;" + self.ENTER 
        cabeceraClase += "using System.Transactions;" + self.ENTER 
        cabeceraClase += "using Util;" + 2*self.ENTER 

        return cabeceraClase

    def __generarCuerpoClase(self):
        cuerpoClase = ""

        cuerpoClase += 2*self.TAB + "#region MEF" + self.ENTER 
        cuerpoClase += 2*self.TAB + "[Import]" + self.ENTER 
        cuerpoClase += 2*self.TAB + "private I" + self.__nombreTabla + "Repository _" + self.__nombreTabla + "Repository { get; set; }" + self.ENTER 
        cuerpoClase += 2*self.TAB + "#endregion" + 2*self.ENTER 
        cuerpoClase += 2*self.TAB + "#region Constructor" + self.ENTER 
        cuerpoClase += self.__generarConstructorClase() + self.ENTER 
        cuerpoClase += 2*self.TAB + "#endregion" + 2*self.ENTER 
        cuerpoClase += 2*self.TAB + "#region Methods Public" + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoCreate() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoEdit() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoDelete() + 2*self.ENTER 
        cuerpoClase += self.__generarMetodoObtenerByID() + 2*self.ENTER
        cuerpoClase += self.__generarMetodoObtenerByPagination() + self.ENTER
        cuerpoClase += 2*self.TAB + "#endregion" + 2*self.ENTER 
        
        return cuerpoClase
    
    def __generarConstructorClase(self):
        constructorClase = ""
        constructorClase += 2*self.TAB + "public " + self.__nombreClase + "()" + self.ENTER
        constructorClase += 2*self.TAB + "{" + self.ENTER
        constructorClase += 3*self.TAB + "_" + self.__nombreTabla + "Repository = MEFContainer.Container.GetExport<I" + self.__nombreTabla + "Repository>();" + self.ENTER
        constructorClase += 2*self.TAB + "}" + self.ENTER

        return constructorClase
    
    def __generarMetodoCreate(self):
        metodoCreate = ""
        nombreVariable = "Id" + self.__nombreTabla

        metodoCreate += 2*self.TAB + "public int Create" + self.__nombreTabla + "(" + self.__nombreTabla + "Entity " + self.__nombreTabla + ")" + self.ENTER
        metodoCreate += 2*self.TAB + "{" + self.ENTER 
        metodoCreate += 3*self.TAB + "int " + nombreVariable + " = 0;" + self.ENTER 
        metodoCreate += 3*self.TAB + "bool exito = false;" + self.ENTER 
        metodoCreate += 3*self.TAB + "using (TransactionScope tx = new TransactionScope())" + self.ENTER 
        metodoCreate += 3*self.TAB + "{" + self.ENTER 
        metodoCreate += 4*self.TAB + nombreVariable + " = _" + self.__nombreTabla + "Repository.Insert" + self.__nombreTabla + "(" + self.__nombreTabla + ");" + self.ENTER 
        metodoCreate += 4*self.TAB + "exito = true;" + self.ENTER 
        metodoCreate += 4*self.TAB + "if (exito) tx.Complete();" + self.ENTER 
        metodoCreate += 3*self.TAB + "}" + self.ENTER 
        metodoCreate += 3*self.TAB + "return " + nombreVariable + ";" + self.ENTER 
        metodoCreate += 2*self.TAB + "}" + self.ENTER

        return metodoCreate
    
    def __generarMetodoEdit(self):
        metodoEdit = ""
        metodoEdit += 2*self.TAB + "public bool Edit" + self.__nombreTabla + "(" + self.__nombreTabla + "Entity " + self.__nombreTabla + ")" + self.ENTER
        metodoEdit += 2*self.TAB + "{" + self.ENTER 
        metodoEdit += 3*self.TAB + "bool exito = false;" + self.ENTER 
        metodoEdit += 3*self.TAB + "using (TransactionScope tx = new TransactionScope())" + self.ENTER 
        metodoEdit += 3*self.TAB + "{" + self.ENTER 
        metodoEdit += 4*self.TAB + "exito = _" + self.__nombreTabla + "Repository.Update" + self.__nombreTabla + "(" + self.__nombreTabla + ")" + self.ENTER 
        metodoEdit += 4*self.TAB + "if (exito) tx.Complete();" + self.ENTER 
        metodoEdit += 3*self.TAB + "}" + self.ENTER 
        metodoEdit += 3*self.TAB + "return exito;" + self.ENTER 
        metodoEdit += 2*self.TAB + "}" + self.ENTER

        return metodoEdit
    
    def __generarMetodoDelete(self):
        metodoDelete = ""
        parametrosEntrada = ""
        parametrosDelete = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            parametrosEntrada += valor["tipoDatoNET"] + self.ESPACIO + valor["nombreCampo"] + ","
            parametrosDelete += valor["nombreCampo"] + ","
        
        parametrosEntrada = gestionArchivos.extraerUltimoCaracter(parametrosEntrada)

        metodoDelete += 2*self.TAB + "public bool Delete" + self.__nombreTabla + "(" + parametrosEntrada + ")" + self.ENTER
        metodoDelete += 2*self.TAB + "{" + self.ENTER 
        metodoDelete += 3*self.TAB + "bool exito = false;" + self.ENTER 
        metodoDelete += 3*self.TAB + "exito = _" + self.__nombreTabla + "Repository.Delete" + self.__nombreTabla + "(" + parametrosDelete + ");" + self.ENTER 
        metodoDelete += 3*self.TAB + "return exito;" + self.ENTER 
        metodoDelete += 2*self.TAB + "}" + self.ENTER

        return metodoDelete
    
    def __generarMetodoObtenerByID(self):
        metodoObtenerByID = ""
        parametrosEntrada = ""
        parametrosFiltro = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            parametrosEntrada += valor["tipoDatoNET"] + self.ESPACIO + valor["nombreCampo"] + ","
            parametrosFiltro += valor["nombreCampo"] + " = " + valor["nombreCampo"] + ","
        
        parametrosEntrada = gestionArchivos.extraerUltimoCaracter(parametrosEntrada)

        metodoObtenerByID += 2*self.TAB + "public " + self.__nombreTabla + "Entity GetById(" + parametrosEntrada + ")" + self.ENTER
        metodoObtenerByID += 2*self.TAB + "{" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + self.__nombreTabla + "Entity " + self.__nombreTabla + " = null;" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + self.__nombreTabla + " = _" + self.__nombreTabla + "Repository.GetItem" + self.__nombreTabla + "(new " + self.__nombreTabla + "Filter() { " + parametrosFiltro + " }, " + self.__nombreTabla + "FilterItemType.ById);" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + "return "+ self.__nombreTabla +";" + self.ENTER 
        metodoObtenerByID += 2*self.TAB + "}" + self.ENTER

        return metodoObtenerByID
    
    def __generarMetodoObtenerByPagination(self):
        MetodoObtenerByPagination = ""
        MetodoObtenerByPagination += 2*self.TAB + "public IEnumerable<" + self.__nombreTabla + "Entity> GetByPagination(" + self.__nombreTabla + "Filter filter, " + self.__nombreTabla + "FilterLstItemType filterType, Pagination pagination)" + self.ENTER
        MetodoObtenerByPagination += 2*self.TAB + "{" + self.ENTER 
        MetodoObtenerByPagination += 3*self.TAB + "List<" + self.__nombreTabla + "Entity> lst = null;" + self.ENTER 
        MetodoObtenerByPagination += 3*self.TAB + "lst = _" + self.__nombreTabla + "Repository.GetLstItem" + self.__nombreTabla + "(filter, filterType, pagination).ToList();" + self.ENTER 
        MetodoObtenerByPagination += 3*self.TAB + "return lst;" + self.ENTER 
        MetodoObtenerByPagination += 2*self.TAB + "}" + self.ENTER

        return MetodoObtenerByPagination