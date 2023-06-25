from objDataAPP import *
from objDataBD import *
from util.enumerados import claseObjeto

#nombreTabla = "Adm_BankQuestion"
class generarObjetos:

    def __init__(self, nombreTabla : str):
        self.nombreTabla = nombreTabla

    def generarObjetosBackEnd(self):
        clase = objetoEntity(self.nombreTabla, claseObjeto.entity)
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