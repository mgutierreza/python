import pyodbc as pyo
import pandas as pd
from ..obtenerConexionBD import consultaDatos
from ..utilitarios import util
from os import remove

TAB = "\t"
ENTER = "\n"

def generarNombreProcedimientoAlmacenado(nombreTabla):
    return nombreTabla + "_Get"


def generarNombreArchivoProcedimientoAlmacenado(nombreProcimientoAlmacenado):
    return nombreProcimientoAlmacenado + ".sql"

    
def generarCabeceraProcedimientoAlmacenado(nombreTabla):
    libreriaProcedimientoAlmacenado = "SET ANSI_NULLS ON" + ENTER + "GO" + ENTER + "SET QUOTED_IDENTIFIER ON" + ENTER + "GO" + 2*ENTER
    cabeceraProcedimientoAlmacenado = ""
    parametrosEntradaProcedimientoAlmacenado = ""

    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    numeroRegistroDiccionario = len(df)

    for i in df.index:
        if (numeroRegistroDiccionario > 1):
            if (df["tipoDato"][i] == 'INT'):
                parametrosEntradaProcedimientoAlmacenado = parametrosEntradaProcedimientoAlmacenado + 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + " = 0,"
            else:
                parametrosEntradaProcedimientoAlmacenado = parametrosEntradaProcedimientoAlmacenado + 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i] + ") = 'null',"
        else:
            if (df["tipoDato"][i] == 'INT'):
                parametrosEntradaProcedimientoAlmacenado = 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + " = 0,"
            else:
                parametrosEntradaProcedimientoAlmacenado = 2*TAB + "@"+ df["nombreCampo"][i] + TAB + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i] + ") = 'null',"
    
    parametrosEntradaProcedimientoAlmacenado = util.extraerUltimoCaracter(parametrosEntradaProcedimientoAlmacenado) + ENTER

    cabeceraProcedimientoAlmacenado = libreriaProcedimientoAlmacenado + "CREATE PROCEDURE dbo." + generarNombreProcedimientoAlmacenado(nombreTabla) + ENTER + "(" + ENTER
    cabeceraProcedimientoAlmacenado = cabeceraProcedimientoAlmacenado + parametrosEntradaProcedimientoAlmacenado + ")" + ENTER + "AS" + ENTER + TAB + "BEGIN" + ENTER
    
    return cabeceraProcedimientoAlmacenado

def generarCondicionalProcedimientoAlmacenado(nombreTabla):
    df = consultaDatos.obtenerMetaDataClavePrincipal(nombreTabla)
    estructuraControlSQLIF = ""
    
    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            estructuraControlSQLIF = 2*TAB + "IF (@"+ df["nombreCampo"][i] +" > 0)" + ENTER
        else:
            estructuraControlSQLIF = 2*TAB + "IF (@"+ df["nombreCampo"][i] +" = 'null')" + ENTER

    return estructuraControlSQLIF


def generarConsultaProcedimientoAlmacenado(nombreTabla):
    
    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)
    lineaCodigoProcedimientoAlmacenado = ""
    consultaProcedimientoAlmacenado = ""
    
    for i in df.index:
        lineaCodigoProcedimientoAlmacenado = lineaCodigoProcedimientoAlmacenado + 5*TAB + nombreTabla + '.' + df["nombreCampo"][i] + "," + ENTER
    
    lineaCodigoProcedimientoAlmacenado = util.extraerUltimoCaracter(lineaCodigoProcedimientoAlmacenado) + ENTER
    consultaProcedimientoAlmacenado = 4*TAB + "SELECT" + ENTER + lineaCodigoProcedimientoAlmacenado 
    consultaProcedimientoAlmacenado = consultaProcedimientoAlmacenado + 4*TAB + "FROM " + "dbo." + nombreTabla + " WITH(NOLOCK)" + ENTER

    return consultaProcedimientoAlmacenado


def crearSPConsultaDatos(nombreTabla):
    

    nombreProcedimientoAlmacenado = generarNombreProcedimientoAlmacenado(nombreTabla)
    nombreArchivoProcedimientoAlmacenado = generarNombreArchivoProcedimientoAlmacenado(nombreProcedimientoAlmacenado)

    cabeceraProcedimientoAlmacenado = generarCabeceraProcedimientoAlmacenado(nombreTabla)
    condicionalProcedimientoAlmacenado = generarCondicionalProcedimientoAlmacenado(nombreTabla)
    consultaProcedimientoAlmacenado = generarConsultaProcedimientoAlmacenado(nombreTabla)

    comandoInicioEstructura = 3*TAB + "BEGIN" + ENTER
    comandoFinEstructura = 3*TAB + "END" + ENTER
    estructuraControlSQLELSE = 2*TAB + "ELSE" + ENTER 
    comandoFinProcedimientoAlmacenado = TAB + "END"

    procedimientoAlmacenado = cabeceraProcedimientoAlmacenado + condicionalProcedimientoAlmacenado + comandoInicioEstructura
    procedimientoAlmacenado = procedimientoAlmacenado + consultaProcedimientoAlmacenado + comandoFinEstructura + estructuraControlSQLELSE 
    procedimientoAlmacenado = procedimientoAlmacenado + comandoInicioEstructura + consultaProcedimientoAlmacenado + comandoFinEstructura 
    procedimientoAlmacenado = procedimientoAlmacenado + comandoFinProcedimientoAlmacenado
    
    remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivoProcedimientoAlmacenado,'w')
    f.write(procedimientoAlmacenado)
    f.close()
