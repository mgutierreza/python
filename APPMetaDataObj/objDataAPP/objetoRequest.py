from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from util.utilitario import gestionArchivos

class objetoRequest(iObjetoAplicacion):

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
        clase += "namespace EP_AcademicMicroservice.Entities" + self.ENTER 
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

        cuerpoClase += self.TAB + "public class " + self.__nombreTabla + "Request : OperationRequest<"+ self.__nombreTabla +"Entity>" + self.ENTER
        cuerpoClase += self.TAB + "{" + 2*self.ENTER 
        cuerpoClase += self.TAB + "}" + 2*self.ENTER
        
        cuerpoClase += self.TAB + "public class " + self.__nombreTabla + "ItemRequest : FilterItemRequest<" + self.__nombreTabla +"Filter, " + self.__nombreTabla + "FilterItemType>" + self.ENTER
        cuerpoClase += self.TAB + "{" + 2*self.ENTER 
        cuerpoClase += self.TAB + "}" + 2*self.ENTER

        cuerpoClase += self.TAB + "public class " + self.__nombreTabla + "LstItemRequest : FilterLstItemRequest<" + self.__nombreTabla +"Filter, " + self.__nombreTabla + "FilterLstItemType>" + self.ENTER
        cuerpoClase += self.TAB + "{" + 2*self.ENTER 
        cuerpoClase += self.TAB + "}" + 2*self.ENTER

        return cuerpoClase
