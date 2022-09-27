import os
from os import remove
from enumerados import tipoObjeto, claseObjeto

def extraerUltimoCaracter(texto):
    last_char_index = texto.rfind(",")
    texto = texto[:last_char_index]

    return texto


def generarRutaArchivo(nombreTabla, tipoObjeto):

    rutaCreacionArchivo = "d:\\Clases\\"

    if (tipoObjeto.BaseDatos):
        rutaCreacionArchivo = rutaCreacionArchivo + nombreTabla + "\\APP"
    else:
        rutaCreacionArchivo = rutaCreacionArchivo +nombreTabla + "\\BD"

    if (not os.path.isdir(rutaCreacionArchivo)):
        os.makedirs(rutaCreacionArchivo)

    return rutaCreacionArchivo


def generarNombreArchivo(nombreTablaBaseDatos, claseObjeto):

    nombreArchivo = ""

    if(claseObjeto.entity):
        nombreArchivo = nombreTablaBaseDatos + "Entity"
    elif(claseObjeto.exception):
        nombreArchivo = nombreTablaBaseDatos + "Exception"
    elif(claseObjeto.filter):
        nombreArchivo = nombreTablaBaseDatos + "Filter"
    elif(claseObjeto.filterType):
        nombreArchivo = nombreTablaBaseDatos + "FilterType"
    elif(claseObjeto.request):
        nombreArchivo = nombreTablaBaseDatos + "Request"
    elif(claseObjeto.response):
        nombreArchivo = nombreTablaBaseDatos + "Response"
    elif(claseObjeto.requestValidation):
        nombreArchivo = nombreTablaBaseDatos + "RequestValidation"
    elif(claseObjeto.service):
        nombreArchivo = nombreTablaBaseDatos + "Service"
    elif(claseObjeto.repository):
        nombreArchivo = nombreTablaBaseDatos + "Repository"
    elif(claseObjeto.iRepository):
        nombreArchivo = "I" + nombreTablaBaseDatos + "Repository"
    elif(claseObjeto.domain):
        nombreArchivo = nombreTablaBaseDatos + "Domain"
    elif(claseObjeto.controller):
        nombreArchivo = nombreTablaBaseDatos + "Controller"
    elif(claseObjeto.select):
        nombreArchivo = nombreTablaBaseDatos + "_Get"
    elif(claseObjeto.insert):
        nombreArchivo = nombreTablaBaseDatos + "_Insert"
    elif(claseObjeto.delete):
        nombreArchivo = nombreTablaBaseDatos + "_Delete"
    elif(claseObjeto.update):
        nombreArchivo = nombreTablaBaseDatos + "_Update"
    else:
        nombreArchivo = nombreArchivo
	    
    return nombreArchivo

def generarExtensionArchivo(nombreArchivo, tipoObjeto):
    
    extensionArchivo = ".cs"
    if (tipoObjeto.BaseDatos):
        extensionArchivo = ".sql"

    return nombreArchivo + extensionArchivo

def generarArchivo(rutaArchivo, nombreArchivo, contenidoArchivo):

    rutayNombreArchivo = rutaArchivo + "\\" + nombreArchivo

    if (os.path.isdir(rutaArchivo)):
        remove(rutayNombreArchivo)

    f = open (rutayNombreArchivo,'w')
    f.write(contenidoArchivo)
    f.close()

    return 

