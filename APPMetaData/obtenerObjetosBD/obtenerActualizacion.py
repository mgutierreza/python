import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"
ESPACIO = " "

def generarProcedimientoAlmacenadoActualizacion(nombreTabla):

    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.update)
    extensionArchivo = generarExtensionArchivo(tipoObjeto.BaseDatos)
    contenidoArchivo = generarProcedimientoAlmacenado(nombreTabla)

    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return 

def generarProcedimientoAlmacenado(nombreTabla):
    procedimientoAlmacenado = ""
    
    procedimientoAlmacenado += generarLibreriasProcedimientoAlmacenado()
    procedimientoAlmacenado += generarCabeceraProcedimientoAlmacenado(nombreTabla)
    procedimientoAlmacenado += generarCuerpoProcedimientoAlmacenado(nombreTabla)        

    return procedimientoAlmacenado

def generarLibreriasProcedimientoAlmacenado():
    libreriasProcedimientoAlmacenado = ""
    libreriasProcedimientoAlmacenado += "SET ANSI_NULLS ON" + ENTER 
    libreriasProcedimientoAlmacenado += "GO" + ENTER 
    libreriasProcedimientoAlmacenado += "SET QUOTED_IDENTIFIER ON" + ENTER
    libreriasProcedimientoAlmacenado += "GO" + 2*ENTER

    return libreriasProcedimientoAlmacenado

def generarCabeceraProcedimientoAlmacenado(nombreTabla):
    cabeceraProcedimientoAlmacenado = ""
    cabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, claseObjeto.update) + ENTER
    cabeceraProcedimientoAlmacenado += "(" + ENTER
    cabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)      
    cabeceraProcedimientoAlmacenado += ")" + ENTER 
    cabeceraProcedimientoAlmacenado += "AS" + ENTER
    cabeceraProcedimientoAlmacenado += "BEGIN" + ENTER
    
    return cabeceraProcedimientoAlmacenado

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    
    cuerpoProcedimientoAlmacenado += 4*TAB + "UPDATE dbo." + nombreTabla + ENTER
    cuerpoProcedimientoAlmacenado += 4*TAB + "SET" + ENTER
    cuerpoProcedimientoAlmacenado += generarCamposParaActualizar(nombreTabla)
    cuerpoProcedimientoAlmacenado +=  4*TAB + "WHERE" + ENTER
    cuerpoProcedimientoAlmacenado += generarCamposParaFiltro(nombreTabla)
    cuerpoProcedimientoAlmacenado += "END" + ENTER

    return cuerpoProcedimientoAlmacenado

def generarCamposParaActualizar(nombreTabla):
    camposParaActualizar = ""
    espacioEstandar = 30

    df = obtenerParametrosParaActualizacion(nombreTabla)

    for i in df.index:
        espacioCampo = len(df["nombreCampo"][i])
        espacioFaltante = espacioEstandar - espacioCampo     
        if(df["tipoCampo"][i] != "PRIMARY KEY"):
            if ((df["tipoDato"][i] == 'DATETIME') and ("Update","Upd" in df["nombreCampo"][i])):
                camposParaActualizar += 5*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + espacioFaltante*ESPACIO + "=" + 2*TAB + "GETDATE()," + ENTER
            else:
                camposParaActualizar += 5*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + espacioFaltante*ESPACIO + "=" + 2*TAB + "@" + df["nombreCampo"][i] + "," + ENTER
    
    camposParaActualizar = util.extraerUltimoCaracter(camposParaActualizar) + ENTER

    return camposParaActualizar

def generarCamposParaFiltro(nombreTabla):
    camposParaFiltro = ""
    espacioEstandar = 30

    df =  consultaDatos.obtenerMetaDataClavePrincipalBD(nombreTabla)

    for i in df.index:
        espacioCampo = len(df["nombreCampo"][i])
        espacioFaltante = espacioEstandar - espacioCampo
        camposParaFiltro += 5*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + espacioFaltante*ESPACIO + "=" + 2*TAB + "@" + df["nombreCampo"][i] + ENTER
    
    return camposParaFiltro

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""
    espacioEstandar = 30

    df = obtenerParametrosParaActualizacion(nombreTabla)
    for i in df.index:
        if ((df["tipoDato"][i] == 'DATETIME') and ("Update","Upd" in df["nombreCampo"][i])):
            parametrosEntrada += ""
        else:
            espacioCampo = len(df["nombreCampo"][i])
            espacioFaltante = espacioEstandar - espacioCampo
            if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME' or df["tipoDato"][i] == 'BIGINT'):
                parametrosEntrada += 5*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 2*TAB + df["tipoDato"][i] + "," + ENTER
            else:
                parametrosEntrada += 5*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 2*TAB + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i].astype(str) + ")," + ENTER

    parametrosEntrada = util.extraerUltimoCaracter(parametrosEntrada) + ENTER

    return parametrosEntrada

def obtenerParametrosParaActualizacion(nombreTabla):

    df = consultaDatos.obtenerMetaDataTodosCamposBD(nombreTabla)

    numeroCampos = len(df.index)
    rangoMenor = numeroCampos - 6
    rangoMayor = numeroCampos - 3
    df = df.drop(range(rangoMenor,rangoMayor))
    numeroCampos = len(df.index)

    return df