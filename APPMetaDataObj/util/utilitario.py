import os
from os import remove
from util.enumerados import tipoObjeto, claseObjeto

class gestionArchivos():

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__tipoObjeto = ""
    
    def generarArchivo(self, contenidoArchivo):
        self.__generarTipoObjeto(self)
        
        rutayNombreArchivo = self.__generarRutaArchivo(self) + "\\" + self.generarNombreArchivo(self) + self.__generarExtensionArchivo(self)

        if (os.path.isdir(rutayNombreArchivo)):
            remove(rutayNombreArchivo)

        f = open (rutayNombreArchivo,'w')
        f.write(contenidoArchivo)
        f.close()


    def generarNombreArchivo(self):
        nombreArchivo = ""

        if(self.__claseObjeto == claseObjeto.entity):
            nombreArchivo = self.__nombreTabla + "Entity"
        elif(self.__claseObjeto == claseObjeto.exception):
            nombreArchivo = self.__nombreTabla + "Exception"
        elif(self.__claseObjeto == claseObjeto.filter):
            nombreArchivo = self.__nombreTabla + "Filter"
        elif(self.__claseObjeto == claseObjeto.filterType):
            nombreArchivo = self.__nombreTabla + "FilterType"
        elif(self.__claseObjeto == claseObjeto.request):
            nombreArchivo = self.__nombreTabla + "Request"
        elif(self.__claseObjeto == claseObjeto.response):
            nombreArchivo = self.__nombreTabla + "Response"
        elif(self.__claseObjeto == claseObjeto.requestValidation):
            nombreArchivo = self.__nombreTabla + "RequestValidation"
        elif(self.__claseObjeto == claseObjeto.service):
            nombreArchivo = self.__nombreTabla + "Service"
        elif(self.__claseObjeto == claseObjeto.repository):
            nombreArchivo = self.__nombreTabla + "Repository"
        elif(self.__claseObjeto == claseObjeto.iRepository):
            nombreArchivo = "I" + self.__nombreTabla + "Repository"
        elif(self.__claseObjeto == claseObjeto.domain):
            nombreArchivo = self.__nombreTabla + "Domain"
        elif(self.__claseObjeto == claseObjeto.controller):
            nombreArchivo = self.__nombreTabla + "Controller"
        elif(self.__claseObjeto == claseObjeto.select):
            nombreArchivo = self.__nombreTabla + "_Get"
        elif(self.__claseObjeto == claseObjeto.insert):
            nombreArchivo = self.__nombreTabla + "_Insert"
        elif(self.__claseObjeto == claseObjeto.delete):
            nombreArchivo = self.__nombreTabla + "_Delete"
        elif(self.__claseObjeto == claseObjeto.update):
            nombreArchivo = self.__nombreTabla + "_Update"
        else:
            nombreArchivo = self.__nombreTabla
            
        return nombreArchivo

    def __generarTipoObjeto(self):
        
        self.__tipoObjeto = tipoObjeto.Aplicacion

        if ((self.__claseObjeto == claseObjeto.delete) or
             (self.__claseObjeto == claseObjeto.insert) or
              (self.__claseObjeto == claseObjeto.insert) or 
              (self.__claseObjeto == claseObjeto.select)):
            self.__tipoObjeto = tipoObjeto.BaseDatos
        
        return
    
    def __generarRutaArchivo(self):
        rutaCreacionArchivo = "d:\\Clases\\"

        if (self.__tipoObjeto == tipoObjeto.BaseDatos):
            rutaCreacionArchivo = rutaCreacionArchivo + self.__nombreTabla + "\\BD"
        else:
            rutaCreacionArchivo = rutaCreacionArchivo + self.__nombreTabla + "\\AP"

        if (not os.path.isdir(rutaCreacionArchivo)):
            os.makedirs(rutaCreacionArchivo)

        return rutaCreacionArchivo
    
    def __generarExtensionArchivo(self):
        extensionArchivo = ".cs"
        if (self.__tipoObjeto == tipoObjeto.BaseDatos):
            extensionArchivo = ".sql"
               
        return extensionArchivo



    



