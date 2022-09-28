import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"

def generarProcedimientoAlmacenadoInsercion(nombreTabla):

    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.insert)
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
    CabeceraProcedimientoAlmacenado = ""
    CabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, claseObjeto.insert) + ENTER 
    CabeceraProcedimientoAlmacenado += "(" + ENTER 
    CabeceraProcedimientoAlmacenado += generarParametrosSalidaProcedimientoAlmacenado(nombreTabla)       
    CabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)       
    CabeceraProcedimientoAlmacenado += ")" + ENTER
    CabeceraProcedimientoAlmacenado += "AS" + ENTER
    CabeceraProcedimientoAlmacenado += "BEGIN" + ENTER

    return CabeceraProcedimientoAlmacenado

def generarParametrosSalidaProcedimientoAlmacenado(nombreTabla):
    parametrosSalida = ""
    
    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME'):
            parametrosSalida += 2*TAB + "@"+ df["nombreCampo"][i] + 10*TAB + df["tipoDato"][i] + " OUTPUT," + ENTER
        else:
            parametrosSalida += 2*TAB + "@"+ df["nombreCampo"][i] + 10*TAB + df["tipoDato"][i] + "(" + (df["tamanhoCampo"][i]).astype(str) + ") OUTPUT," + ENTER

    parametrosSalida = util.extraerUltimoCaracter(parametrosSalida) + ENTER

    return parametrosSalida

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""

    df = obtenerParametrosParaInsercion(nombreTabla)
    for i in df.index:
        if (df["tipoCampo"][i] == "CAMPO"):
            if ((df["tipoDato"][i] == 'DATETIME') and ("Registro" in df["nombreCampo"][i])):
                parametrosEntrada += ""
            else:
                if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME'):
                    parametrosEntrada += 2*TAB + "@"+ df["nombreCampo"][i] + 10*TAB + df["tipoDato"][i] + "," + ENTER
                else:
                    parametrosEntrada += 2*TAB + "@"+ df["nombreCampo"][i] + 10*TAB + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i].astype(str) + ")," + ENTER

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
            if (df["tipoCampo"][i] == "CAMPO"):
                if ((df["tipoDato"][i] == 'DATETIME') and ("Registro" in df["nombreCampo"][i])):
                    parametrosInsercion += 10*TAB + "GETDATE()," + ENTER
                else:
                    parametrosInsercion += 10*TAB + "@"+ df["nombreCampo"][i] + "," + ENTER
        
    if (tipoParametro == "campo"):
        for i in df.index:
            if (df["tipoCampo"][i] == "CAMPO"):
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


