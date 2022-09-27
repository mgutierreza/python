import os
from os import remove
from .enumerados import *

def extraerUltimoCaracter(texto):
    last_char_index = texto.rfind(",")
    texto = texto[:last_char_index]

    return texto


def generarRutaArchivo(nombreTabla, tipoObjeto):

    rutaCreacionArchivo = "d:\\Clases\\"

    if (tipoObjeto.BaseDatos):
        rutaCreacionArchivo = rutaCreacionArchivo + nombreTabla + "\\BD"
    else:
        rutaCreacionArchivo = rutaCreacionArchivo +nombreTabla + "\\AP"

    if (not os.path.isdir(rutaCreacionArchivo)):
        os.makedirs(rutaCreacionArchivo)

    return rutaCreacionArchivo


def generarNombreArchivo(nombreTablaBaseDatos, claseObjeto):

    nombreArchivo = ""

    if(claseObjeto == claseObjeto.entity):
        nombreArchivo = nombreTablaBaseDatos + "Entity"
    elif(claseObjeto == claseObjeto.exception):
        nombreArchivo = nombreTablaBaseDatos + "Exception"
    elif(claseObjeto == claseObjeto.filter):
        nombreArchivo = nombreTablaBaseDatos + "Filter"
    elif(claseObjeto == claseObjeto.filterType):
        nombreArchivo = nombreTablaBaseDatos + "FilterType"
    elif(claseObjeto == claseObjeto.request):
        nombreArchivo = nombreTablaBaseDatos + "Request"
    elif(claseObjeto == claseObjeto.response):
        nombreArchivo = nombreTablaBaseDatos + "Response"
    elif(claseObjeto == claseObjeto.requestValidation):
        nombreArchivo = nombreTablaBaseDatos + "RequestValidation"
    elif(claseObjeto == claseObjeto.service):
        nombreArchivo = nombreTablaBaseDatos + "Service"
    elif(claseObjeto == claseObjeto.repository):
        nombreArchivo = nombreTablaBaseDatos + "Repository"
    elif(claseObjeto == claseObjeto.iRepository):
        nombreArchivo = "I" + nombreTablaBaseDatos + "Repository"
    elif(claseObjeto == claseObjeto.domain):
        nombreArchivo = nombreTablaBaseDatos + "Domain"
    elif(claseObjeto == claseObjeto.controller):
        nombreArchivo = nombreTablaBaseDatos + "Controller"
    elif(claseObjeto == claseObjeto.select):
        nombreArchivo = nombreTablaBaseDatos + "_Get"
    elif(claseObjeto == claseObjeto.insert):
        nombreArchivo = nombreTablaBaseDatos + "_Insert"
    elif(claseObjeto == claseObjeto.delete):
        nombreArchivo = nombreTablaBaseDatos + "_Delete"
    elif(claseObjeto == claseObjeto.update):
        nombreArchivo = nombreTablaBaseDatos + "_Update"
    else:
        nombreArchivo = nombreArchivo
	    
    return nombreArchivo

def generarExtensionArchivo(tipoObjeto):
    extensionArchivo = ".cs"

    if (tipoObjeto.BaseDatos):
        extensionArchivo = ".sql"

    return extensionArchivo

def generarArchivo(rutaArchivo, nombreArchivo, contenidoArchivo):
    rutayNombreArchivo = rutaArchivo + "\\" + nombreArchivo

    if (os.path.isdir(rutayNombreArchivo)):
        remove(rutayNombreArchivo)

    f = open (rutayNombreArchivo,'w')
    f.write(contenidoArchivo)
    f.close()

    return 

