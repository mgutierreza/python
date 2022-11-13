from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from objConexionBD.consultasBD import obtenerData
from util.utilitario import gestionArchivos

class objetoIRepository(iObjetoAplicacion):

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreClase = ''
        self.__claseEntity = self.__nombreTabla + "Entity"
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
        clase += "namespace EP_AcademicMicroservice.Repository" + self.ENTER 
        clase += "{" + self.ENTER
        clase += self.TAB + "public interface " + self.__nombreClase + " : IGenericRepository<" + self.__claseEntity + ">" + self.ENTER
        clase += self.TAB + "{" + self.ENTER         
        clase += self.__generarCuerpoClase()
        clase += self.TAB + "}" + self.ENTER 
        clase += "}" + self.ENTER
        return clase
 
    def __generarCabeceraClase(self):
        cabeceraClase = ""
        cabeceraClase += "using System;" + self.ENTER 
        cabeceraClase += "using System.Collections.Generic;" + self.ENTER
        cabeceraClase += "using System.Linq;" + self.ENTER 
        cabeceraClase += "using System.Text;" + self.ENTER
        cabeceraClase += "using System.Threading.Tasks;" + self.ENTER
        cabeceraClase += "using EP_AcademicMicroservice.Entities;" + 2*self.ENTER
        return cabeceraClase

    def __generarCuerpoClase(self):
        cuerpoClase = ""
        camposPK = ""
        dictData = {}
               
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            camposPK = str(valor['tipoDatoNET']) + self.ESPACIO + str(valor['nombreCampo']) + "," + self.ESPACIO

        camposPK = gestionArchivos.extraerUltimoCaracter(camposPK)

        cuerpoClase += 2*self.TAB + "int Insert" + self.__nombreTabla + "(" + self.__claseEntity + " item);" + self.ENTER 
        cuerpoClase += 2*self.TAB + "bool Update" + self.__nombreTabla + "(" + self.__claseEntity + " item);" + self.ENTER 
        cuerpoClase += 2*self.TAB + "bool Delete" + self.__nombreTabla + "(" + camposPK + ");" + self.ENTER 
        cuerpoClase += 2*self.TAB + self.__claseEntity + " GetItem" + self.__nombreTabla + "(" + self.__nombreTabla + "Filter filter, " + self.__nombreTabla + "FilterItemType filterType);" + self.ENTER 
        cuerpoClase += 2*self.TAB + "IEnumerable<" + self.__claseEntity + "> GetLstItem" + self.__nombreTabla + "(" + self.__nombreTabla + "Filter filter, " + self.__nombreTabla + "FilterLstItemType filterType, Pagination pagination);" + self.ENTER 
        return cuerpoClase
