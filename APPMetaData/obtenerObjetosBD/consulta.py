import pyodbc as pyo
import pandas as pd
from ..utilitarios.util import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from ..utilitarios.enumerados import tipoObjeto, claseObjeto

from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"

def generarArchivoSelect(nombreTabla):
    rutayNombreArchivo = generarRutaArchivo(nombreTabla, tipoObjeto.BaseDatos)
    nombreArchivo = generarNombreArchivo(nombreTabla, claseObjeto.select)
    extensionArchivo = generarExtensionArchivo(nombreArchivo, tipoObjeto.BaseDatos)
    contenidoArchivo = generarProcedimientoAlmacenado(nombreTabla)
    
    generarArchivo(rutayNombreArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

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
    
    cabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + generarNombreArchivo(nombreTabla, claseObjeto.select) + ENTER 
    cabeceraProcedimientoAlmacenado += "(" + ENTER
    cabeceraProcedimientoAlmacenado += generarParametrosEntradaProcedimientoAlmacenado(nombreTabla)
    cabeceraProcedimientoAlmacenado += ")" + ENTER
    cabeceraProcedimientoAlmacenado += "AS" + ENTER 

    return cabeceraProcedimientoAlmacenado

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = TAB + "BEGIN" + ENTER
    cuerpoProcedimientoAlmacenado += generarCondicionalProcedimientoAlmacenado(nombreTabla)
    cuerpoProcedimientoAlmacenado += TAB + "END" + ENTER

    return cuerpoProcedimientoAlmacenado

def generarParametrosEntradaProcedimientoAlmacenado(nombreTabla):
    parametrosEntrada = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    numeroRegistroDiccionario = len(df)

    for i in df.index:
        if (numeroRegistroDiccionario > 1):
            if (df["tipoDato"][i] == 'INT'):
                parametrosEntrada += + 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + " = 0,"
            else:
                parametrosEntrada += + 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i] + ") = 'null',"
        else:
            if (df["tipoDato"][i] == 'INT'):
                parametrosEntrada = 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + " = 0,"
            else:
                parametrosEntrada = 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i] + ") = 'null',"
    
    parametrosEntrada = util.extraerUltimoCaracter(parametrosEntrada) + ENTER    
    return parametrosEntrada

def generarCondicionalProcedimientoAlmacenado(nombreTabla):
    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    condicionalProcedimientoAlmacenado = ""
    
    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            condicionalProcedimientoAlmacenado += 2*TAB + "IF (@"+ df["nombreCampo"][i] +" > 0)" + ENTER
        else:
            condicionalProcedimientoAlmacenado += 2*TAB + "IF (@"+ df["nombreCampo"][i] +" = 'null')" + ENTER
    
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
    
    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)
    lineaCodigoProcedimientoAlmacenado = ""
    consultaProcedimientoAlmacenado = 4*TAB + "SELECT" + ENTER
    
    for i in df.index:
        lineaCodigoProcedimientoAlmacenado += 5*TAB + nombreTabla + '.' + df["nombreCampo"][i] + "," + ENTER
    
    consultaProcedimientoAlmacenado += util.extraerUltimoCaracter(lineaCodigoProcedimientoAlmacenado) + ENTER
    consultaProcedimientoAlmacenado += 4*TAB + "FROM " + "dbo." + nombreTabla + " WITH(NOLOCK)" + ENTER

    return consultaProcedimientoAlmacenado

def generarFiltroConsulta(nombreTabla):
    
    dfClave = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    lineaFiltroCodigoProcedimientoAlmacenado = 4*TAB + "WHERE"

    for i in dfClave.index:
        lineaFiltroCodigoProcedimientoAlmacenado += 2*TAB + nombreTabla + "."+ dfClave["nombreCampo"][i] + TAB + "=" + TAB + "@" + dfClave["nombreCampo"][i] + ENTER
    
    return lineaFiltroCodigoProcedimientoAlmacenado

