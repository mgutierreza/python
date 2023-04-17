from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from util.utilitario import gestionArchivos

class objetoRequestvalidator(iObjetoAplicacion):

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
        clase += "namespace EP_AcademicMicroservice.Service" + self.ENTER 
        clase += "{" + self.ENTER
        clase += self.TAB + "public static class " + self.__nombreClase + self.ENTER
        clase += self.TAB + "{" + self.ENTER 
        clase += self.__generarCuerpoClase()
        clase +=  self.TAB + "}" + self.ENTER
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

        cuerpoClase +=  2*self.TAB + "#region Validate" + self.ENTER
        cuerpoClase +=  2*self.TAB + "public static void ValidateRequest(this " + self.__nombreTabla + "Response response, " + self.__nombreTabla + "Request request)" + self.ENTER
        cuerpoClase +=  2*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "if (request.Item == null)" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  4*self.TAB + "response.LstError.Add(\"Se requiere la entidad Estructura\");" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "}" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "if (string.IsNullOrEmpty(request.ServerName))" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  4*self.TAB + "response.LstError.Add(\"No se identifico el servidor de origen para la solicitud\");" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "}" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "if (string.IsNullOrEmpty(request.UserName))" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  4*self.TAB + "response.LstError.Add(\"No se identifico el usuario que realizo la solicitud\");" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "}" + self.ENTER
        cuerpoClase +=  2*self.TAB + "}" + self.ENTER
        cuerpoClase +=  2*self.TAB + "#endregion" + 2*self.ENTER

        cuerpoClase +=  2*self.TAB + "#region Initialize" + self.ENTER
        cuerpoClase +=  2*self.TAB + "public static void InitializeResponse(this " + self.__nombreTabla + "Response response, " + self.__nombreTabla + "Request request)" + self.ENTER
        cuerpoClase +=  2*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.Ticket = request.Ticket;" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.ServerName = request.ServerName;" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.UserName = request.UserName;" + self.ENTER                 
        cuerpoClase +=  2*self.TAB + "}" + 2*self.ENTER             
                
        cuerpoClase +=  2*self.TAB + "public static void InitializeResponse(this " + self.__nombreTabla + "ItemResponse response, " + self.__nombreTabla + "ItemRequest request)" + self.ENTER
        cuerpoClase +=  2*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.Ticket = request.Ticket;" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.ServerName = request.ServerName;" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.UserName = request.UserName;" + self.ENTER                 
        cuerpoClase +=  2*self.TAB + "}" + 2*self.ENTER             
        
        cuerpoClase +=  2*self.TAB + "public static void InitializeResponse(this " + self.__nombreTabla + "LstItemResponse response, " + self.__nombreTabla + "LstItemRequest request)" + self.ENTER
        cuerpoClase +=  2*self.TAB + "{" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.Ticket = request.Ticket;" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.ServerName = request.ServerName;" + self.ENTER 
        cuerpoClase +=  3*self.TAB + "response.UserName = request.UserName;" + self.ENTER                 
        cuerpoClase +=  3*self.TAB + "response.Pagination = request.Pagination;" + self.ENTER 
        cuerpoClase +=  2*self.TAB + "}" + self.ENTER             
        cuerpoClase +=  2*self.TAB + "#endregion" + self.ENTER
        
        return cuerpoClase
