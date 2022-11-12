from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from objConexionBD.consultasBD import obtenerData
from util.utilitario import gestionArchivos

class objetoFilter(iObjetoAplicacion):

    def __init__(self,nombreTabla, claseObjeto):
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
        clase += "namespace EP_AcademicMicroservice.Entities" + self.ENTER 
        clase += "{" + self.ENTER
        clase += self.TAB + "public class " + self.__nombreClase + self.ENTER
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
        cabeceraClase += "using System.Threading.Tasks;" + 2*self.ENTER
        return cabeceraClase

    def __generarCuerpoClase(self):
        cuerpoClase = ""
        dictData = {}
               
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            cuerpoClase += 2*self.TAB + "public " + valor['tipoDatoNET'] + self.ESPACIO + str(valor['nombreCampo']) + self.ESPACIO + "{ get; set; }" + self.ENTER

        return cuerpoClase
