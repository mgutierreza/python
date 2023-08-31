import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo 
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"

def generarProcedimientoAlmacenadoSelect(nombreTabla):
    rutaArchivo = generarRutaArchivo('QUERY', enumerados.tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.select)
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
    cabeceraProcedimientoAlmacenado = ""
    
    cabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, enumerados.claseObjeto.select) + ENTER 
    cabeceraProcedimientoAlmacenado += "(" + ENTER
    cabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)
    cabeceraProcedimientoAlmacenado += ")" + ENTER
    cabeceraProcedimientoAlmacenado += "AS" + ENTER 

    return cabeceraProcedimientoAlmacenado

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""
    parametrosEntradaPK = ""

    numeroClaves = consultaDatos.obtenerNumeroMetaDataClaves()
    
    if (numeroClaves > 0):
        df = consultaDatos.obtenerMetaDataClavePrincipal()
       
        if (len(df.index) > 0):
            for i in df.index:
                    if (df["tipoDatoBD"][i] == 'INT' or df["tipoDatoBD"][i] == 'BIGINT' or df["tipoDatoBD"][i] == 'SMALLINT' or df["tipoDatoBD"][i] == 'TINYINT'):
                        parametrosEntradaPK += 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDatoBD"][i] + " = 0," + ENTER
                    else:
                        parametrosEntradaPK += 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDatoBD"][i] + "(" + str(df["tamanhoCampo"][i]) + ") = 'null'," + ENTER
        else:
            df = consultaDatos.obtenerMetaDataClaveForanea()
            for i in df.index:
                if (df["tipoDatoBD"][i] == 'INT' or df["tipoDatoBD"][i] == 'BIGINT' or df["tipoDatoBD"][i] == 'SMALLINT' or df["tipoDatoBD"][i] == 'TINYINT'):
                    parametrosEntradaPK += 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDatoBD"][i] + " = 0," + ENTER
                else:
                    parametrosEntradaPK += 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDatoBD"][i] + "(" + str(df["tamanhoCampo"][i]) + ") = 'null'," + ENTER
        parametrosEntrada = util.extraerUltimoCaracter(parametrosEntradaPK) + ENTER 
    else:
        parametrosEntrada = ""

    return parametrosEntrada

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    
    cuerpoProcedimientoAlmacenado = ""
    numeroClaves = consultaDatos.obtenerNumeroMetaDataClaves()
        
    if (numeroClaves > 0):    
        cuerpoProcedimientoAlmacenado = TAB + "BEGIN" + ENTER
        cuerpoProcedimientoAlmacenado += generarCondicionalProcedimientoAlmacenado(nombreTabla)
        cuerpoProcedimientoAlmacenado += TAB + "END" + ENTER
    else:
        cuerpoProcedimientoAlmacenado = TAB + "BEGIN" + ENTER
        cuerpoProcedimientoAlmacenado += generarConsultaProcedimientoAlmacenado(nombreTabla)
        cuerpoProcedimientoAlmacenado += TAB + "END" + ENTER

    return cuerpoProcedimientoAlmacenado

def generarCondicionalProcedimientoAlmacenado(nombreTabla):
    df = consultaDatos.obtenerMetaDataClavePrincipal()
    condicionalProcedimientoAlmacenado = 2*TAB + "IF ("
    
    for i in df.index:
        if (df["tipoDatoBD"][i] == 'INT' or df["tipoDatoBD"][i] == 'BIGINT' or df["tipoDatoBD"][i] == 'SMALLINT' or df["tipoDatoBD"][i] == 'TINYINT'):
            condicionalProcedimientoAlmacenado += "@"+ df["nombreCampo"][i] +" > 0 AND " 
        else:
            condicionalProcedimientoAlmacenado += "@"+ df["nombreCampo"][i] +" <> 'null' AND "
    
    condicionalProcedimientoAlmacenado = util.extraerUltimaPalabra(condicionalProcedimientoAlmacenado, "AND") 
    condicionalProcedimientoAlmacenado += ")" + ENTER
    condicionalProcedimientoAlmacenado += 3*TAB + "BEGIN" + ENTER
    condicionalProcedimientoAlmacenado += generarConsultaProcedimientoAlmacenado(nombreTabla)
    condicionalProcedimientoAlmacenado += generarFiltroConsulta(nombreTabla)
    condicionalProcedimientoAlmacenado += 3*TAB + "END" + ENTER
    condicionalProcedimientoAlmacenado += 2*TAB + "ELSE" + ENTER
    condicionalProcedimientoAlmacenado += 3*TAB + "BEGIN" + ENTER
    condicionalProcedimientoAlmacenado += generarConsultaProcedimientoAlmacenado(nombreTabla)
    condicionalProcedimientoAlmacenado += 3*TAB + "END" + ENTER

    return condicionalProcedimientoAlmacenado

def generarConsultaProcedimientoAlmacenado(nombreTabla):
    
    df = consultaDatos.obtenerMetaDataTodosCampos()
    lineaCodigoProcedimientoAlmacenado = ""
    consultaProcedimientoAlmacenado = 4*TAB + "SELECT" + ENTER
    
    for i in df.index:
        lineaCodigoProcedimientoAlmacenado += 5*TAB + nombreTabla + '.' + df["nombreCampo"][i] + "," + ENTER
    
    consultaProcedimientoAlmacenado += util.extraerUltimoCaracter(lineaCodigoProcedimientoAlmacenado) + ENTER
    consultaProcedimientoAlmacenado += 4*TAB + "FROM " + "dbo." + nombreTabla + " WITH(NOLOCK)" + ENTER

    return consultaProcedimientoAlmacenado

def generarFiltroConsulta(nombreTabla):
    filtroConsulta = 4*TAB + "WHERE " + ENTER
    filtroLineaConsulta = ""

    dfClave = consultaDatos.obtenerMetaDataClavePrincipal()
    numeroRegistroDiccionario = len(dfClave)
    
    if (numeroRegistroDiccionario > 0):    
        for i in dfClave.index:
            filtroLineaConsulta += 5*TAB + nombreTabla + "."+ dfClave["nombreCampo"][i] + TAB + "=" + TAB + "@" + dfClave["nombreCampo"][i] + " AND " + ENTER
    else:
        dfClave = consultaDatos.obtenerMetaDataClaveForanea()
        for i in dfClave.index:
            filtroLineaConsulta += 5*TAB + nombreTabla + "."+ dfClave["nombreCampo"][i] + TAB + "=" + TAB + "@" + dfClave["nombreCampo"][i] + " AND " + ENTER
    
    filtroConsulta += util.extraerUltimaPalabra(filtroLineaConsulta, "AND") + ENTER

    return filtroConsulta

