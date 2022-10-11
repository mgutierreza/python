from objDataAPP import *
from util.enumerados import claseObjeto

nombreTabla = "AcdCampus"

def ejecutar():
    clase = objetoEntity(nombreTabla, claseObjeto.entity)
    clase.generarArchivo()

    clase = objetoException(nombreTabla, claseObjeto.exception)
    clase.generarArchivo()

    clase = objetoFilter(nombreTabla, claseObjeto.filter)
    clase.generarArchivo()

    clase = objetoFilterType(nombreTabla, claseObjeto.filterType)
    clase.generarArchivo()

    clase = objetoRequest(nombreTabla, claseObjeto.request)
    clase.generarArchivo()

    clase = objetoResponse(nombreTabla, claseObjeto.response)
    clase.generarArchivo()

    clase = objetoRequestValidator(nombreTabla, claseObjeto.requestValidation)
    clase.generarArchivo()

    clase = objetoIRepository(nombreTabla, claseObjeto.iRepository)
    clase.generarArchivo()

    clase = objetoRepository(nombreTabla, claseObjeto.repository)
    clase.generarArchivo()

    return