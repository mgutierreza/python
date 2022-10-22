import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"
ESPACIO = " "

def generarProcedimientoAlmacenadoActualizacion(nombreTabla):

    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.update)
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
    cabeceraProcedimientoAlmacenado = ""
    cabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.update) + ENTER
    cabeceraProcedimientoAlmacenado += "(" + ENTER
    cabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)      
    cabeceraProcedimientoAlmacenado += ")" + ENTER 
    cabeceraProcedimientoAlmacenado += "AS" + ENTER
    cabeceraProcedimientoAlmacenado += "BEGIN" + ENTER
    
    return cabeceraProcedimientoAlmacenado

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    existeClaveForanea = False
    
    df = consultaDatos.obtenerMetaDataFK(nombreTabla)
    
    if (len(df) > 0 ):
        existeClaveForanea = True
        cuerpoProcedimientoAlmacenado += TAB + "DECLARE @existeRegistro INT = 0" + 2*ENTER

    if (existeClaveForanea):
        for i in df.index:
            cuerpoProcedimientoAlmacenado += TAB + "SELECT @existeRegistro = " + df["columnaOrigen"][i] + " FROM dbo." + df["tablaOrigen"][i] + " WITH(NOLOCK) WHERE " + df["columnaOrigen"][i] + " = @" + df["columnaDestino"][i] + 2*ENTER
            cuerpoProcedimientoAlmacenado += TAB + "IF @existeRegistro <= 0" + ENTER
            cuerpoProcedimientoAlmacenado += TAB + "BEGIN" + ENTER
            cuerpoProcedimientoAlmacenado += 2*TAB + "SET @errorCode = CONCAT(@errorCode, '/', 'not_found_record_" + df["tablaOrigen"][i] + "/'" + ENTER
            cuerpoProcedimientoAlmacenado += TAB + "END" + 2*ENTER
            cuerpoProcedimientoAlmacenado += TAB + "IF @existeRegistro > 0" + ENTER
            cuerpoProcedimientoAlmacenado += TAB + "BEGIN" + ENTER
            
    cuerpoProcedimientoAlmacenado += 4*TAB + "UPDATE dbo." + nombreTabla + ENTER
    cuerpoProcedimientoAlmacenado += 4*TAB + "SET" + ENTER
    cuerpoProcedimientoAlmacenado += generarCamposParaActualizar(nombreTabla)
    cuerpoProcedimientoAlmacenado +=  4*TAB + "WHERE" + ENTER
    cuerpoProcedimientoAlmacenado += generarCamposParaFiltro(nombreTabla)
    
    if (existeClaveForanea):
        cuerpoProcedimientoAlmacenado += TAB + "END" + ENTER   
    
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
            if ((df["tipoDatoBD"][i] == 'DATETIME') and ("Update","Upd" in df["nombreCampo"][i])):
                camposParaActualizar += 5*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + espacioFaltante*ESPACIO + "=" + 2*TAB + "GETDATE()," + ENTER
            else:
                camposParaActualizar += 5*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + espacioFaltante*ESPACIO + "=" + 2*TAB + "@" + df["nombreCampo"][i] + "," + ENTER
    
    camposParaActualizar = util.extraerUltimoCaracter(camposParaActualizar) + ENTER

    return camposParaActualizar

def generarCamposParaFiltro(nombreTabla):
    camposParaFiltro = ""
    espacioEstandar = 30

    df =  consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)

    for i in df.index:
        espacioCampo = len(df["nombreCampo"][i])
        espacioFaltante = espacioEstandar - espacioCampo
        camposParaFiltro += 5*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + espacioFaltante*ESPACIO + "=" + 2*TAB + "@" + df["nombreCampo"][i] + ENTER
    
    return camposParaFiltro

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""
    espacioEstandar = 30
    espacioFaltante = 0

    df = obtenerParametrosParaActualizacion(nombreTabla)
    for i in df.index:
        if ((df["tipoDatoBD"][i] == 'DATETIME') and ("Update","Upd" in df["nombreCampo"][i])):
            parametrosEntrada += ""
        else:
            espacioCampo = len(df["nombreCampo"][i])
            espacioFaltante = espacioEstandar - espacioCampo
            if (df["tamanhoCampo"][i] == 0):
                parametrosEntrada += 5*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 2*TAB + df["tipoDatoBD"][i] + "," + ENTER
            else:
                parametrosEntrada += 5*TAB + "@"+ df["nombreCampo"][i] + espacioFaltante*ESPACIO + 2*TAB + df["tipoDatoBD"][i] + "(" + df["tamanhoCampo"][i].astype(str) + ")," + ENTER
    #parametrosEntrada = util.extraerUltimoCaracter(parametrosEntrada) + ENTER
    espacioCampo = 10
    espacioFaltante = espacioEstandar - espacioCampo
    parametrosEntrada += 5*TAB + "@errorCode" + espacioFaltante*ESPACIO + 2*TAB + "VARCHAR(150) = '' OUTPUT" + ENTER

    return parametrosEntrada

def obtenerParametrosParaActualizacion(nombreTabla):

    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)

    numeroCampos = len(df.index)
    rangoMenor = numeroCampos - 6
    rangoMayor = numeroCampos - 3
    df = df.drop(range(rangoMenor,rangoMayor))
    numeroCampos = len(df.index)

    return df