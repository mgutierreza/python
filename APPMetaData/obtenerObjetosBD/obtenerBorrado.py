import pyodbc as pyo
import pandas as pd
from obtenerObjetosBD import obtenerConsulta
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"

def generarProcedimientoAlmacenadoBorrado(nombreTabla):

    rutaArchivo = generarRutaArchivo('DELETE', enumerados.tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.delete)
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
    libreriasProcedimientoAlmacenado = "USE BDEpartners_DEV" + ENTER 
    libreriasProcedimientoAlmacenado += "GO" + ENTER 
    libreriasProcedimientoAlmacenado += "SET ANSI_NULLS ON" + ENTER 
    libreriasProcedimientoAlmacenado += "GO" + ENTER 
    libreriasProcedimientoAlmacenado += "SET QUOTED_IDENTIFIER ON" + ENTER
    libreriasProcedimientoAlmacenado += "GO" + 2*ENTER
    return libreriasProcedimientoAlmacenado    

def generarCabeceraProcedimientoAlmacenado(nombreTabla):
    CabeceraProcedimientoAlmacenado = ""
    CabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.delete) + ENTER 
    CabeceraProcedimientoAlmacenado += "(" + ENTER
    CabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)
    CabeceraProcedimientoAlmacenado += ")" + ENTER   
    CabeceraProcedimientoAlmacenado += "AS" + ENTER
    CabeceraProcedimientoAlmacenado += "BEGIN" + ENTER
    return CabeceraProcedimientoAlmacenado

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    campoEstado = ""

    campoEstado = obtenerCampoEstadoTabla(nombreTabla)

    if (campoEstado == ""):
        
        cuerpoProcedimientoAlmacenado += 6*TAB + "DELETE FROM " + nombreTabla + ENTER
        cuerpoProcedimientoAlmacenado += 6*TAB + "WHERE dbo." 
        cuerpoProcedimientoAlmacenado += obtenerFiltros(nombreTabla) + ENTER

    else:
        variable = "@variableEstado"
        cuerpoProcedimientoAlmacenado += 4*TAB + "DECLARE " + variable + " INT = " + ENTER
        cuerpoProcedimientoAlmacenado += 6*TAB +"(" + ENTER
        cuerpoProcedimientoAlmacenado += generarConsultaComprobacion(nombreTabla)
        cuerpoProcedimientoAlmacenado += 6*TAB +")" + 2*ENTER
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

    df = consultaDatos.obtenerMetaDataClavePrincipal()

    if (len(df.index) == 0):
        df = consultaDatos.obtenerMetaDataClaves()

    for i in df.index:
        if (df["tamanhoCampo"][i] == 0):
            parametrosEntrada += 2*TAB +"@"+ df["nombreCampo"][i] + 4*TAB + df["tipoDatoBD"][i] + "," + ENTER
        else:
            parametrosEntrada += 2*TAB +"@"+ df["nombreCampo"][i] + 4*TAB + df["tipoDatoBD"][i] + "(" + (df["tamanhoCampo"][i]).astype(str) + ")," + ENTER
    
    parametrosEntrada = util.extraerUltimoCaracter(parametrosEntrada) + ENTER
    
    return parametrosEntrada

def generarConsultaComprobacion(nombreTabla):
    consultaComprobacion = ""
    campoEstado = ""
    campoClavePrincipal = ""
    
    campoEstado = obtenerCampoEstadoTabla(nombreTabla)
    campoClavePrincipal = obtenerClavePrincipalTabla(nombreTabla)

    consultaComprobacion += 7*TAB + "SELECT " + campoEstado + ENTER
    consultaComprobacion += 7*TAB + "FROM dbo." + nombreTabla + ENTER
    consultaComprobacion += 7*TAB + "WHERE " + ENTER
    consultaComprobacion += obtenerFiltros(nombreTabla) + ENTER

    return consultaComprobacion

def generarActualizacionEstado(nombreTabla, estadoRegistro = 0):
    actualizacionEstado = ""
    campoEstado = obtenerCampoEstadoTabla(nombreTabla)

    actualizacionEstado += 7*TAB + "UPDATE dbo." + nombreTabla + ENTER 
    actualizacionEstado += 7*TAB + "SET " + nombreTabla + "." + campoEstado + TAB + "=" + TAB + str(estadoRegistro) + ENTER
    actualizacionEstado += 7*TAB + "WHERE " + ENTER
    actualizacionEstado += obtenerFiltros(nombreTabla) + ENTER
    
    return actualizacionEstado

def obtenerClavePrincipalTabla(nombreTabla): 
    campoClavePrincipal = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal()

    for i in df.index:
        campoClavePrincipal += df["nombreCampo"][i]
   
    return campoClavePrincipal

def obtenerCampoEstadoTabla(nombreTabla):
    campoEstado = ""

    df = consultaDatos.obtenerMetaDataCamposSinClavePrincipal()

    for i in df.index:
        if ((df["tipoDatoBD"][i] == 'INT' or df["tipoDatoBD"][i] == 'SMALLINT' or df["tipoDatoBD"][i] == 'TINYINT') and ("Estado" in df["nombreCampo"][i])):
            campoEstado += df["nombreCampo"][i]

    return campoEstado

def obtenerFiltros(nombreTabla):
    filtros = ""
    filtrosClave = ""

    dfClave = consultaDatos.obtenerMetaDataClavePrincipal()
    numeroRegistroDiccionario = len(dfClave)
    
    if (numeroRegistroDiccionario > 0):    
        for i in dfClave.index:
            filtrosClave += 8*TAB + nombreTabla + "." + dfClave["nombreCampo"][i] + TAB + "=" + TAB + "@" + dfClave["nombreCampo"][i] + " AND " + ENTER
    else:
        dfClave = consultaDatos.obtenerMetaDataClaves()
        for i in dfClave.index:
            filtrosClave += 8*TAB + nombreTabla + "." + dfClave["nombreCampo"][i] + TAB + "=" + TAB + "@" + dfClave["nombreCampo"][i] + " AND " + ENTER
    
    filtros += util.extraerUltimaPalabra(filtrosClave, "AND")


    return filtros