import pyodbc as pyo
import pandas as pd
import os
from obtenerObjetosBD import generarProcedimientoAlmacenadoSelect, generarProcedimientoAlmacenadoInsercion, generarProcedimientoAlmacenadoActualizacion

nombreTablaBaseDatos = "AcdCampus"

#Creación de Objetos de Base de Datos
generarProcedimientoAlmacenadoSelect("AcdCampus")
generarProcedimientoAlmacenadoInsercion("AcdCampus")
generarProcedimientoAlmacenadoActualizacion("AcdCampus")

#crearSPInserciónDatos("AcdCampus")
#crearSPActualizacionDatos("AcdCampus")
#crearSPEliminacionDatos("AcdCampus")


#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
#generarArchivoController("AcdCampus")



