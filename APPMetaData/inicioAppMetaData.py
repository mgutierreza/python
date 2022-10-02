from obtenerObjetosBD import *
from obtenerObjetosAPP import *

nombreTablaBaseDatos = "AcdCampus"

#Creación de Objetos de Base de Datos
generarProcedimientoAlmacenadoSelect(nombreTablaBaseDatos)
generarProcedimientoAlmacenadoInsercion(nombreTablaBaseDatos)
generarProcedimientoAlmacenadoActualizacion(nombreTablaBaseDatos)
generarProcedimientoAlmacenadoBorrado(nombreTablaBaseDatos)

#Creación de Objetos de Aplicación
generarArchivoEntity(nombreTablaBaseDatos)
generarArchivoException(nombreTablaBaseDatos)
generarArchivoFilter(nombreTablaBaseDatos)
generarArchivoFilterType(nombreTablaBaseDatos)

#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
#generarArchivoController("AcdCampus")



