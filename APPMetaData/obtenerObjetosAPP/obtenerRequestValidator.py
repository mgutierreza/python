from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados

TAB = "\t"
ENTER = "\n"

def generarArchivoRequestValidator(nombreTabla):
    rutaArchivo = generarRutaArchivo('12_REQUESTVALIDATION', enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.requestValidation)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace " + getNombreProyecto() + "Microservice.Service" + ENTER 
    claseEntity += "{"  + ENTER   
    claseEntity += generarCuerpoClase(nombreTabla)
    claseEntity += "}"

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using " + getNombreProyecto() + "Microservice.Entities;" + ENTER 
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""

    cuerpoClase += TAB + "public static class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.requestValidation) + ENTER
    cuerpoClase += TAB + "{" + ENTER 
   
    cuerpoClase +=  2*TAB + "#region Validate" + ENTER
    cuerpoClase +=  2*TAB + "public static void ValidateRequest(this " + nombreTabla + "Response response, " + nombreTabla + "Request request)" + ENTER
    cuerpoClase +=  2*TAB + "{" + ENTER 
    cuerpoClase +=  3*TAB + "if (request.Item == null)" + ENTER 
    cuerpoClase +=  3*TAB + "{" + ENTER 
    cuerpoClase +=  4*TAB + "response.LstError.Add(\"Se requiere la entidad Estructura\");" + ENTER 
    cuerpoClase +=  3*TAB + "}" + ENTER 
    cuerpoClase +=  3*TAB + "if (string.IsNullOrEmpty(request.ServerName))" + ENTER 
    cuerpoClase +=  3*TAB + "{" + ENTER 
    cuerpoClase +=  4*TAB + "response.LstError.Add(\"No se identifico el servidor de origen para la solicitud\");" + ENTER 
    cuerpoClase +=  3*TAB + "}" + ENTER 
    cuerpoClase +=  3*TAB + "if (string.IsNullOrEmpty(request.UserName))" + ENTER 
    cuerpoClase +=  3*TAB + "{" + ENTER 
    cuerpoClase +=  4*TAB + "response.LstError.Add(\"No se identifico el usuario que realizo la solicitud\");" + ENTER 
    cuerpoClase +=  3*TAB + "}" + ENTER
    cuerpoClase +=  2*TAB + "}" + ENTER
    cuerpoClase +=  2*TAB + "#endregion" + 2*ENTER

    cuerpoClase +=  2*TAB + "#region Initialize" + ENTER
    cuerpoClase +=  2*TAB + "public static void InitializeResponse(this " + nombreTabla + "Response response, " + nombreTabla + "Request request)" + ENTER
    cuerpoClase +=  2*TAB + "{" + ENTER 
    cuerpoClase +=  3*TAB + "response.Ticket = request.Ticket;" + ENTER 
    cuerpoClase +=  3*TAB + "response.ServerName = request.ServerName;" + ENTER 
    cuerpoClase +=  3*TAB + "response.UserName = request.UserName;" + ENTER                 
    cuerpoClase +=  2*TAB + "}" + 2*ENTER             
            
    cuerpoClase +=  2*TAB + "public static void InitializeResponse(this " + nombreTabla + "ItemResponse response, " + nombreTabla + "ItemRequest request)" + ENTER
    cuerpoClase +=  2*TAB + "{" + ENTER 
    cuerpoClase +=  3*TAB + "response.Ticket = request.Ticket;" + ENTER 
    cuerpoClase +=  3*TAB + "response.ServerName = request.ServerName;" + ENTER 
    cuerpoClase +=  3*TAB + "response.UserName = request.UserName;" + ENTER                 
    cuerpoClase +=  2*TAB + "}" + 2*ENTER             
    
    cuerpoClase +=  2*TAB + "public static void InitializeResponse(this " + nombreTabla + "LstItemResponse response, " + nombreTabla + "LstItemRequest request)" + ENTER
    cuerpoClase +=  2*TAB + "{" + ENTER 
    cuerpoClase +=  3*TAB + "response.Ticket = request.Ticket;" + ENTER 
    cuerpoClase +=  3*TAB + "response.ServerName = request.ServerName;" + ENTER 
    cuerpoClase +=  3*TAB + "response.UserName = request.UserName;" + ENTER                 
    cuerpoClase +=  3*TAB + "response.Pagination = request.Pagination;" + ENTER 
    cuerpoClase +=  2*TAB + "}" + ENTER             
    cuerpoClase +=  2*TAB + "#endregion" + ENTER
    cuerpoClase +=  TAB + "}" + ENTER

    return cuerpoClase
