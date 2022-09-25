import pyodbc as pyo
import pandas as pd
import os
from consulta import crearSPConsultaDatos
from insercion import crearSPInserciónDatos
from actualizacion import crearSPActualizacionDatos
from borrado import crearSPEliminacionDatos
from obtenerController import generarArchivoController

nombreTablaBaseDatos = "AcdCampus"

rutaGeneral = "d:\\Clases\\"
rutaGeneralAPP = rutaGeneral + nombreTablaBaseDatos + "\\APP"
rutaGeneralBD = rutaGeneral +nombreTablaBaseDatos + "\\BD"

if (not os.path.isdir(rutaGeneral)):
    os.makedirs(rutaGeneral)

if (not os.path.isdir(rutaGeneralAPP)):
    os.makedirs(rutaGeneralAPP)

if (not os.path.isdir(rutaGeneralBD)):
    os.makedirs(rutaGeneralBD)



#Creación de Objetos de Base de Datos
#crearSPConsultaDatos("AcdCampus")
#crearSPInserciónDatos("AcdCampus")
#crearSPActualizacionDatos("AcdCampus")
#crearSPEliminacionDatos("AcdCampus")


#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
generarArchivoController("AcdCampus")



