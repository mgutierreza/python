import pyodbc as pyo
import pandas as pd
import os
from obtenerObjetosBD import generarProcedimientoAlmacenadoSelect, generarProcedimientoAlmacenadoInsercion

nombreTablaBaseDatos = "AcdCampus"

#Creación de Objetos de Base de Datos
generarProcedimientoAlmacenadoSelect("AcdCampus")
generarProcedimientoAlmacenadoInsercion("AcdCampus")

#crearSPInserciónDatos("AcdCampus")
#crearSPActualizacionDatos("AcdCampus")
#crearSPEliminacionDatos("AcdCampus")


#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
#generarArchivoController("AcdCampus")



