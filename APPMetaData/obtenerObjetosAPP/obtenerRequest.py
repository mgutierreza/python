from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto

TAB = "\t"
ENTER = "\n"

def generarArchivoRequest(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.request)
    extensionArchivo = generarExtensionArchivo(tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace EP_AcademicMicroservice.Entities" + ENTER 
    claseEntity += "{"  + 2*ENTER   
    claseEntity += generarCuerpoClase(nombreTabla)    
    claseEntity += "}"

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase += "using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase

def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""

    cuerpoClase += TAB + "public class " + nombreTabla + "Request : OperationRequest<"+ nombreTabla +"Entity>" + ENTER
    cuerpoClase += TAB + "{" + 2*ENTER 
    cuerpoClase += TAB + "}" + 2*ENTER
    
    cuerpoClase += TAB + "public class " + nombreTabla + "ItemRequest : FilterItemRequest<" + nombreTabla +"Filter, " + nombreTabla + "FilterItemType>" + ENTER
    cuerpoClase += TAB + "{" + 2*ENTER 
    cuerpoClase += TAB + "}" + 2*ENTER

    cuerpoClase += TAB + "public class " + nombreTabla + "LstItemRequest : FilterLstItemRequest<" + nombreTabla +"Filter, " + nombreTabla + "FilterLstItemType>" + ENTER
    cuerpoClase += TAB + "{" + 2*ENTER 
    cuerpoClase += TAB + "}" + 2*ENTER

    return cuerpoClase

