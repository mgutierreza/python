from objDataAPP import *
from objDataBD import *
from util.enumerados import claseObjeto
from objDataAPP.objetoEntity import objetoEntity
from objDataAPP.objetoException import objetoException
from objDataAPP.objetoFilterType import objetoFilterType
from objDataAPP.objetoRequest import objetoRequest
from objDataAPP.objetoResponse import objetoResponse
from objDataAPP.objetoRequestValidator import objetoRequestValidator
from objDataAPP.objetoIRepository import objetoIRepository
from objDataAPP.objetoRepository import objetoRepository
from objDataAPP.objetoDomain import objetoDomain
from objDataAPP.objetoController import objetoController
from objDataAPP.objetoService import objetoService
from objDataBD.objetoInsertar import objetoInsertar

#nombreTabla = "Adm_BankQuestion"
class GenerarObjetos():

    def __init__(self, nombreTabla):
        self.nombreTabla = nombreTabla

    def generarObjetosBackEnd(self):
        clase = objetoEntity(self.nombreTabla)
        clase.generarArchivo()

        clase = objetoException(self.nombreTabla, claseObjeto.exception)
        clase.generarArchivo()

        clase = objetoFilter(self.nombreTabla, claseObjeto.filter)
        clase.generarArchivo()

        clase = objetoFilterType(self.nombreTabla, claseObjeto.filterType)
        clase.generarArchivo()

        clase = objetoRequest(self.nombreTabla, claseObjeto.request)
        clase.generarArchivo()

        clase = objetoResponse(self.nombreTabla, claseObjeto.response)
        clase.generarArchivo()

        clase = objetoRequestValidator(self.nombreTabla, claseObjeto.requestValidation)
        clase.generarArchivo()

        clase = objetoIRepository(self.nombreTabla, claseObjeto.iRepository)
        clase.generarArchivo()

        clase = objetoRepository(self.nombreTabla, claseObjeto.repository)
        clase.generarArchivo()

        clase = objetoRepository(self.nombreTabla, claseObjeto.service)
        clase.generarArchivo()

        clase = objetoRepository(self.nombreTabla, claseObjeto.domain)
        clase.generarArchivo()

        clase = objetoRepository(self.nombreTabla, claseObjeto.controller)
        clase.generarArchivo()

        clase = objetoProcedimientoInsertar(self.nombreTabla, claseObjeto.insert)
        clase.generarArchivo()

        return