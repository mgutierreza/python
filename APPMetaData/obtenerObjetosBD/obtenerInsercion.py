import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"
ESPACIO = " "

def generarProcedimientoAlmacenadoInsercion(nombreTabla):

    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.insert)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.BaseDatos)
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
    CabeceraProcedimientoAlmacenado = ""
    CabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.insert) + ENTER 
    CabeceraProcedimientoAlmacenado += "(" + ENTER 
    CabeceraProcedimientoAlmacenado += generarParametrosSalidaProcedimientoAlmacenado(nombreTabla)       
    CabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)       
    CabeceraProcedimientoAlmacenado += ")" + ENTER
    CabeceraProcedimientoAlmacenado += "AS" + ENTER
    CabeceraProcedimientoAlmacenado += "BEGIN" + ENTER

    return CabeceraProcedimientoAlmacenado

def generarParametrosSalidaProcedimientoAlmacenado(nombreTabla):
    parametrosSalida = ""
    espacioEstandar = 30

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        espacioCampo = len(df["nombreCampo"][i])
        espacioFaltante = espacioEstandar - espacioCampo 
        if (df["tamanhoCampo"][i] == 0):
            parametrosSalida += 2*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 4*TAB + df["tipoDatoBD"][i] + " OUTPUT," + ENTER
        else:
            parametrosSalida += 2*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 4*TAB + df["tipoDatoBD"][i] + "(" + (df["tamanhoCampo"][i]).astype(str) + ") OUTPUT," + ENTER

    parametrosSalida = util.extraerUltimoCaracter(parametrosSalida) + ENTER

    return parametrosSalida

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""
    espacioEstandar = 30

    df = obtenerParametrosParaInsercion(nombreTabla)
    for i in df.index:
        espacioCampo = len(df["nombreCampo"][i])
        espacioFaltante = espacioEstandar - espacioCampo            
        if (df["tipoCampo"][i] != "PRIMARY KEY"):
            if ((df["tipoDatoBD"][i] == 'DATETIME') and ("Registro" in df["nombreCampo"][i])):
                parametrosEntrada += ""
            else:
                if (df["tamanhoCampo"][i] == 0):
                    parametrosEntrada += 2*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 4*TAB + df["tipoDatoBD"][i] + "," + ENTER
                else:
                    parametrosEntrada += 2*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 4*TAB + df["tipoDatoBD"][i] + "(" + df["tamanhoCampo"][i].astype(str) + ")," + ENTER

    parametrosEntrada = util.extraerUltimoCaracter(parametrosEntrada) + ENTER

    return parametrosEntrada

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    cuerpoProcedimientoAlmacenado += 4*TAB + "INSERT INTO dbo." + nombreTabla + ENTER
    cuerpoProcedimientoAlmacenado += 9*TAB + "(" + ENTER
    cuerpoProcedimientoAlmacenado += obtenerParametrosInsercion(nombreTabla, tipoParametro = "campo") + ENTER
    cuerpoProcedimientoAlmacenado += 9*TAB + ")" + ENTER
    cuerpoProcedimientoAlmacenado += 4*TAB + "VALUES" + ENTER
    cuerpoProcedimientoAlmacenado += 9*TAB + "(" + ENTER
    cuerpoProcedimientoAlmacenado += obtenerParametrosInsercion(nombreTabla, tipoParametro = "valor") + ENTER
    cuerpoProcedimientoAlmacenado += 9*TAB + ")" + ENTER
    cuerpoProcedimientoAlmacenado += obtenerSalidaProcedimientoAlmacenado(nombreTabla)
    cuerpoProcedimientoAlmacenado += "END" + ENTER

    return cuerpoProcedimientoAlmacenado

def obtenerParametrosInsercion(nombreTabla, tipoParametro):
    parametrosInsercion = ""

    df = obtenerParametrosParaInsercion(nombreTabla)

    if (tipoParametro == "valor"):
        for i in df.index:
            if (df["tipoCampo"][i] != "PRIMARY KEY"):
                if ((df["tipoDatoBD"][i] == 'DATETIME') and ("Registro" in df["nombreCampo"][i])):
                    parametrosInsercion += 10*TAB + "GETDATE()," + ENTER
                else:
                    parametrosInsercion += 10*TAB + "@"+ df["nombreCampo"][i] + "," + ENTER
        
    if (tipoParametro == "campo"):
        for i in df.index:
            if (df["tipoCampo"][i] != "PRIMARY KEY"):
                parametrosInsercion += 10*TAB + nombreTabla + "." + df["nombreCampo"][i] + "," + ENTER
      
    parametrosInsercion = util.extraerUltimoCaracter(parametrosInsercion)
    
    return parametrosInsercion

def obtenerSalidaProcedimientoAlmacenado(nombreTabla):
    salidaProcedimientoAlmacenado = ""
        
    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        salidaProcedimientoAlmacenado += 4*TAB + "SET @"+ df["nombreCampo"][i] + TAB + "=" + TAB + "@@IDENTITY" + ENTER

    return salidaProcedimientoAlmacenado


def obtenerParametrosParaInsercion(nombreTabla):

    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)

    numeroCampos = len(df.index)
    rangoMenor = numeroCampos - 3
    rangoMayor = numeroCampos
    df = df.drop(range(rangoMenor,rangoMayor))
    numeroCampos = len(df.index)

    return df


