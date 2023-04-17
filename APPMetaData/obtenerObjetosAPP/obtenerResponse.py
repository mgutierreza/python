from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo, getNombreProyecto
from utilitarios import enumerados

TAB = "\t"
ENTER = "\n"

def generarArchivoResponse(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.Aplicacion)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.response)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.Aplicacion)
    contenidoArchivo = generarClase(nombreTabla)
    
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarClase(nombreTabla):
    claseEntity = ""
    claseEntity += generarCabeceraClase()
    claseEntity += "namespace " + getNombreProyecto() + "Microservice.Entities" + ENTER 
    claseEntity += "{"  + 2*ENTER   
    claseEntity += generarCuerpoClase(nombreTabla)    
    claseEntity +=  "}"

    return claseEntity

def generarCabeceraClase():
    cabeceraClase = ""
    cabeceraClase += "using System;" + ENTER 
    cabeceraClase +="using System.Collections.Generic;" + ENTER
    cabeceraClase += "using System.Linq;" + ENTER 
    cabeceraClase += "using System.Text;" + ENTER
    cabeceraClase += "using System.Threading.Tasks;" + 2*ENTER
    return cabeceraClase


def generarCuerpoClase(nombreTabla):
    cuerpoClase = ""

    cuerpoClase += TAB + "public class " + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.response) + " : ItemResponse<bool>" + ENTER
    cuerpoClase += TAB + "{" + 2*ENTER 
    cuerpoClase += TAB + "}" + 2*ENTER
    
    cuerpoClase += TAB + "public class " + nombreTabla + "ItemResponse : ItemResponse<" + nombreTabla + "Entity>" + ENTER
    cuerpoClase += TAB + "{" + 2*ENTER 
    cuerpoClase += TAB + "}" + 2*ENTER

    cuerpoClase += TAB + "public class " + nombreTabla + "LstItemResponse : LstItemResponse<" + nombreTabla + "Entity>" + ENTER
    cuerpoClase += TAB + "{" + 2*ENTER 
    cuerpoClase += TAB + "}" + 2*ENTER

    return cuerpoClase


