import pyodbc as pyo
import pandas as pd
from consulta import crearSPConsultaDatos
from insercion import crearSPInserciónDatos
from actualizacion import crearSPActualizacionDatos
from borrado import crearSPEliminacionDatos
from obtenerIRepository import generarArchivoIRepository

#Creación de Objetos de Base de Datos
#crearSPConsultaDatos("AcdCampus")
#crearSPInserciónDatos("AcdCampus")
#crearSPActualizacionDatos("AcdCampus")
#crearSPEliminacionDatos("AcdCampus")


#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
generarArchivoIRepository("AcdCampus")



