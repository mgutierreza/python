from objDataAPP import *
from objDataBD import *
from util.enumerados import claseObjeto

'''nombreTabla = "AcdCampus"'''
class generarObjetos():

    def __init__(self, nombreTabla):
        self.__nombreTabla = nombreTabla

    def generarObjetosBackEnd(self):
        clase = objetoEntity(self.__nombreTabla, claseObjeto.entity)
        clase.generarArchivo()

        clase = objetoException(self.__nombreTabla, claseObjeto.exception)
        clase.generarArchivo()

        clase = objetoFilter(self.__nombreTabla, claseObjeto.filter)
        clase.generarArchivo()

        clase = objetoFilterType(self.__nombreTabla, claseObjeto.filterType)
        clase.generarArchivo()

        clase = objetoRequest(self.__nombreTabla, claseObjeto.request)
        clase.generarArchivo()

        clase = objetoResponse(self.__nombreTabla, claseObjeto.response)
        clase.generarArchivo()

        clase = objetoRequestValidator(self.__nombreTabla, claseObjeto.requestValidation)
        clase.generarArchivo()

        clase = objetoIRepository(self.__nombreTabla, claseObjeto.iRepository)
        clase.generarArchivo()

        clase = objetoRepository(self.__nombreTabla, claseObjeto.repository)
        clase.generarArchivo()

        clase = objetoRepository(self.__nombreTabla, claseObjeto.service)
        clase.generarArchivo()

        clase = objetoRepository(self.__nombreTabla, claseObjeto.domain)
        clase.generarArchivo()

        clase = objetoRepository(self.__nombreTabla, claseObjeto.controller)
        clase.generarArchivo()

        clase = objetoProcedimientoInsertar(self.__nombreTabla, claseObjeto.insert)
        clase.generarArchivo()

        return