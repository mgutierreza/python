from objDataAPP.objetoEntity import objetoEntity
from util.enumerados import claseObjeto

nombreTabla = "AcdCampus"

def ejecutar():
    entity = objetoEntity(nombreTabla, claseObjeto.entity)
    entity.generarArchivo()
    return