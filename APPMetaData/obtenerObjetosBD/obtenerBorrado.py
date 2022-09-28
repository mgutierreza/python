import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import tipoObjeto, claseObjeto
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"

def generarProcedimientoAlmacenadoBorrado(nombreTabla):

    rutaArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.delete)
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
    CabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, claseObjeto.delete) + ENTER 
    CabeceraProcedimientoAlmacenado += "(" + ENTER
    CabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)
    CabeceraProcedimientoAlmacenado += ")" + ENTER   
    CabeceraProcedimientoAlmacenado += "AS" + ENTER
    CabeceraProcedimientoAlmacenado += "BEGIN" + ENTER
    return CabeceraProcedimientoAlmacenado

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    variable = "@variableEstado"

    cuerpoProcedimientoAlmacenado += 4*TAB + "DECLARE " + variable + " VARCHAR(50) = " + ENTER
    cuerpoProcedimientoAlmacenado += 9*TAB +"(" + ENTER
    cuerpoProcedimientoAlmacenado += generarConsultaComprobacion(nombreTabla)
    cuerpoProcedimientoAlmacenado += 9*TAB +")" + 2*ENTER
    cuerpoProcedimientoAlmacenado += 4*TAB + "IF (" + variable + " = 0)" + ENTER
    cuerpoProcedimientoAlmacenado += 6*TAB + "BEGIN" + ENTER 
    cuerpoProcedimientoAlmacenado += generarActualizacionEstado(nombreTabla, 1) 
    cuerpoProcedimientoAlmacenado += 6*TAB + "END" + ENTER
    cuerpoProcedimientoAlmacenado += 4*TAB + "ELSE" + ENTER 
    cuerpoProcedimientoAlmacenado += 6*TAB + "BEGIN" + ENTER 
    cuerpoProcedimientoAlmacenado += generarActualizacionEstado(nombreTabla, 0) 
    cuerpoProcedimientoAlmacenado += 6*TAB + "END" + ENTER
    cuerpoProcedimientoAlmacenado += "END" + ENTER
    return cuerpoProcedimientoAlmacenado    

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME'):
            parametrosEntrada += 2*TAB +"@"+ df["nombreCampo"][i] + 4*TAB + df["tipoDato"][i] + "," + ENTER
        else:
            parametrosEntrada += 2*TAB +"@"+ df["nombreCampo"][i] + 4*TAB + df["tipoDato"][i] + "(" + (df["tamanhoCampo"][i]).astype(str) + ")," + ENTER
    
    parametrosEntrada = util.extraerUltimoCaracter(parametrosEntrada) + ENTER
    
    return parametrosEntrada

def generarConsultaComprobacion(nombreTabla):
    consultaComprobacion = ""
    campoEstado = ""
    campoClavePrincipal = ""
    
    campoEstado = obtenerCampoEstadoTabla(nombreTabla)
    campoClavePrincipal = obtenerClavePrincipalTabla(nombreTabla)

    consultaComprobacion += 10*TAB + "SELECT " + campoEstado + ENTER
    consultaComprobacion += 10*TAB + "FROM dbo." + nombreTabla + ENTER
    consultaComprobacion += 10*TAB + "WHERE " + nombreTabla + "." + campoClavePrincipal + TAB + "=" + TAB + "@" + campoClavePrincipal + ENTER

    return consultaComprobacion

def generarActualizacionEstado(nombreTabla, estadoRegistro = 0):
    actualizacionEstado = ""
    campoEstado = obtenerCampoEstadoTabla(nombreTabla)
    campoClavePrincipal = obtenerClavePrincipalTabla(nombreTabla)

    actualizacionEstado += 7*TAB + "UPDATE dbo." + nombreTabla + ENTER 
    actualizacionEstado += 7*TAB + "SET " + nombreTabla + "." + campoEstado + TAB + "=" + TAB + str(estadoRegistro) + ENTER
    actualizacionEstado += 7*TAB + "WHERE " + nombreTabla + "." + campoClavePrincipal + TAB + "=" + TAB + "@" + campoClavePrincipal + ENTER
    
    return actualizacionEstado

def obtenerClavePrincipalTabla(nombreTabla): 
    campoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        campoClavePrincipal += df["nombreCampo"][i]
   
    return campoClavePrincipal

def obtenerCampoEstadoTabla(nombreTabla):
    campoEstado = ""

    df = consultaDatos.obtenerMetaDataCamposSinClavePrincipal(nombreTabla)

    for i in df.index:
        if ((df["tipoDato"][i] == 'INT') and ("Estado" in df["nombreCampo"][i])):
            campoEstado += df["nombreCampo"][i]

    return campoEstado