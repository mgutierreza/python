import pyodbc as pyo
import pandas as pd
from consulta import crearSPConsultaDatos
from insercion import crearSPInserciónDatos
from actualizacion import crearSPActualizacionDatos
from borrado import crearSPEliminacionDatos
from obtenerRepositorio import generarArchivoRepository

#Creación de Objetos de Base de Datos
#crearSPConsultaDatos("AcdCampus")
#crearSPInserciónDatos("AcdCampus")
#crearSPActualizacionDatos("AcdCampus")
#crearSPEliminacionDatos("AcdCampus")


#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
generarArchivoRepository("AcdCampus")



