import pyodbc as pyo
import pandas as pd
import os
from obtenerObjetosBD.consulta import crearSPConsultaDatos
from utilitarios.enumerados import tipoObjeto
from obtenerObjetosBD.insercion import crearSPInserciónDatos
from obtenerObjetosBD.actualizacion import crearSPActualizacionDatos
from obtenerObjetosBD.borrado import crearSPEliminacionDatos
from obtenerObjetosAPP.obtenerController import generarArchivoController

nombreTablaBaseDatos = "AcdCampus"

#Creación de Objetos de Base de Datos
crearSPConsultaDatos("AcdCampus")




#crearSPInserciónDatos("AcdCampus")
#crearSPActualizacionDatos("AcdCampus")
#crearSPEliminacionDatos("AcdCampus")


#Creación de Objetos de Aplicación
#generarArchivoEntity("AcdCampus")
#generarArchivoController("AcdCampus")



