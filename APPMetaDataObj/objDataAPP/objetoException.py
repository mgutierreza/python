from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from util.utilitario import gestionArchivos

class objetoException(iObjetoAplicacion):

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
        clase += "namespace EP_AcademicMicroservice.Exceptions" + self.ENTER 
        clase += "{" + self.ENTER
        clase += self.__generarCuerpoClase()
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
        cuerpoClase = cuerpoClase + self.TAB + "public class " + self.__nombreClase + " : CustomException" + self.ENTER
        cuerpoClase = cuerpoClase + self.TAB + "{" + self.ENTER 
        cuerpoClase = cuerpoClase + 2*self.TAB + "public override string CustomMessage" + self.ENTER
        cuerpoClase = cuerpoClase + 2*self.TAB + "{" + self.ENTER
        cuerpoClase = cuerpoClase + 3*self.TAB + "get" + self.ENTER
        cuerpoClase = cuerpoClase + 3*self.TAB + "{" + self.ENTER
        cuerpoClase = cuerpoClase + 4*self.TAB + "return \"Prueba Fail inserting header\";" + self.ENTER
        cuerpoClase = cuerpoClase + 3*self.TAB + "}" + self.ENTER
        cuerpoClase = cuerpoClase + 2*self.TAB + "}" + self.ENTER
        cuerpoClase = cuerpoClase + self.TAB + "}" + self.ENTER

        return cuerpoClase
