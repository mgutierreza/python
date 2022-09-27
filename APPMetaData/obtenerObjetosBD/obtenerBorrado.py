import pyodbc as pyo
import pandas as pd
from os import remove

TAB = "\t"
ENTER = "\n"

def crearSPEliminacionDatos(nombreTabla):
    procedimientoAlmacenado = ""
    nombreProcedimientoAlmacenado = generarNombreProcedimientoAlmacenado(nombreTabla)
    nombreArchivoProcedimientoAlmacenado = generarNombreArchivoProcedimientoAlmacenado(nombreProcedimientoAlmacenado)
    cabeceraProcedimientoAlmacenado = generarCabeceraProcedimientoAlmacenado(nombreTabla)
    consultaComprobacion = crearConsultaComprobacion(nombreTabla)
    cuerpoProcedimientoAlmacenado = generarCuerpoProcedimientoAlmacenado(nombreTabla)
    
    procedimientoAlmacenado = cabeceraProcedimientoAlmacenado + consultaComprobacion + cuerpoProcedimientoAlmacenado + ENTER + "END"
    
    #remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivoProcedimientoAlmacenado,'w')
    f.write(procedimientoAlmacenado)
    f.close()

    return 

def generarCabeceraProcedimientoAlmacenado(nombreTabla):
    CabeceraProcedimientoAlmacenado = ""
    libreriaProcedimientoAlmacenado = "SET ANSI_NULLS ON" + ENTER + "GO" + ENTER + "SET QUOTED_IDENTIFIER ON" + ENTER + "GO" + 2*ENTER
    inicioCabeceraProcedimientoAlmacenado = "CREATE PROCEDURE dbo." + generarNombreProcedimientoAlmacenado(nombreTabla) + ENTER + "(" + ENTER
    finCabeceraProcedimientoAlmacenado = ")" + ENTER + "AS" + ENTER + "BEGIN" + ENTER
    parametrosClavePrincipal = ""

    
    df = identificarClavePrimaria(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME'):
            parametrosClavePrincipal = parametrosClavePrincipal + 2*TAB +"@"+ df["nombreCampo"][i] + 4*TAB + df["tipoDato"][i] + "," + ENTER
        else:
            parametrosClavePrincipal = parametrosClavePrincipal + 2*TAB +"@"+ df["nombreCampo"][i] + 4*TAB + df["tipoDato"][i] + "(" + (df["tamanhoCampo"][i]).astype(str) + ") OUTPUT," + ENTER

    last_char_index = parametrosClavePrincipal.rfind(",")
    parametrosClavePrincipal = parametrosClavePrincipal[:last_char_index] + ENTER

    CabeceraProcedimientoAlmacenado = libreriaProcedimientoAlmacenado + inicioCabeceraProcedimientoAlmacenado + parametrosClavePrincipal
    CabeceraProcedimientoAlmacenado = CabeceraProcedimientoAlmacenado + finCabeceraProcedimientoAlmacenado

    return CabeceraProcedimientoAlmacenado

def crearConsultaComprobacion(nombreTabla):
    consultaComprobacion = 2*TAB + "DECLARE @estado INT = (" + TAB + "SELECT" + ENTER 
    filtroComandoActualizacion = ""
    camposComandoActualizacion = ""

    df = identificarCampos(nombreTabla)

    for i in df.index:
        if ((df["tipoDato"][i] == 'INT') and ("Estado" in df["nombreCampo"][i])):
            camposComandoActualizacion = nombreTabla + "." + df["nombreCampo"][i] + "," + ENTER

    last_char_index = camposComandoActualizacion.rfind(",")
    camposComandoActualizacion = camposComandoActualizacion[:last_char_index] + ENTER

    df = identificarClavePrimaria(nombreTabla)

    for i in df.index:
        filtroComandoActualizacion = 8*TAB + "WHERE dbo."+ nombreTabla + "." + df["nombreCampo"][i] + " = @" + df["nombreCampo"][i] + " )"
    
    consultaComprobacion = consultaComprobacion + 9*TAB + camposComandoActualizacion
    consultaComprobacion = consultaComprobacion + 8*TAB + "FROM dbo." + nombreTabla + ENTER 
    consultaComprobacion = consultaComprobacion + filtroComandoActualizacion

    return consultaComprobacion

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    comandoActualizacionEstadoActivo = generarActualizacionEstado(nombreTabla, 1)
    comandoActualizacionEstadoInactivo = generarActualizacionEstado(nombreTabla, 0)

    cuerpoProcedimientoAlmacenado = cuerpoProcedimientoAlmacenado + ENTER + 2*TAB + "IF (@estado = 0)" + ENTER + 4*TAB + "BEGIN" + ENTER 
    cuerpoProcedimientoAlmacenado = cuerpoProcedimientoAlmacenado + comandoActualizacionEstadoActivo + ENTER + 4*TAB + "END"
    cuerpoProcedimientoAlmacenado = cuerpoProcedimientoAlmacenado + ENTER + 2*TAB + "ELSE" + ENTER + 4*TAB + "BEGIN" + ENTER
    cuerpoProcedimientoAlmacenado = cuerpoProcedimientoAlmacenado + comandoActualizacionEstadoInactivo + ENTER + 4*TAB + "END"

    return cuerpoProcedimientoAlmacenado    

def generarActualizacionEstado(nombreTabla, estadoRegistro = 0):
    inicioComandoActualizacion = 9*TAB + "UPDATE dbo." + nombreTabla + ENTER + 9*TAB + "SET" + ENTER
    camposComandoActualizacion = ""
    filtroComandoActualizacion = ""

    df = identificarCampos(nombreTabla)

    for i in df.index:
        if ((df["tipoDato"][i] == 'INT') and ("Estado" in df["nombreCampo"][i])):
            camposComandoActualizacion = 10*TAB + "dbo." + nombreTabla + "." + df["nombreCampo"][i] + 1*TAB + "=" + 1*TAB + str(estadoRegistro) + "," + ENTER

    last_char_index = camposComandoActualizacion.rfind(",")
    camposComandoActualizacion = camposComandoActualizacion[:last_char_index] + ENTER

    df = identificarClavePrimaria(nombreTabla)

    for i in df.index:
        filtroComandoActualizacion = filtroComandoActualizacion + 9*TAB + "WHERE" + ENTER + 10*TAB + "dbo."+ nombreTabla + "." + df["nombreCampo"][i] + 1*TAB + "=" + 1*TAB + "@" + df["nombreCampo"][i]

    comandoActualizacionEstado = inicioComandoActualizacion + camposComandoActualizacion + filtroComandoActualizacion

    return comandoActualizacionEstado    



def identificarClavePrimaria(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT b.COLUMN_NAME nombreCampo, UPPER(c.DATA_TYPE) tipoDato, ISNULL(c.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo "
    sql = sql + "FROM information_schema.table_constraints a, information_schema.key_column_usage b, information_schema.columns c "
    sql = sql + "WHERE a.table_name = '" + nombreTabla +"' "
    sql = sql + "AND a.table_name = b.table_name "
    sql = sql + "AND a.table_schema = b.TABLE_SCHEMA "
    sql = sql + "AND a.constraint_name = b.constraint_name "
    sql = sql + "AND b.COLUMN_NAME = c.COLUMN_NAME AND b.TABLE_NAME = c.TABLE_NAME "
    sql = sql + "AND a.CONSTRAINT_TYPE = 'PRIMARY KEY'"
    df = pd.read_sql(sql, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def identificarCampos(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT COLUMN_NAME nombreCampo, upper(DATA_TYPE) tipoDato, isnull(CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo "
    sql = sql + "FROM information_schema.columns "
    sql = sql + "WHERE table_name = '" + nombreTabla + "' AND column_name NOT IN ("
    sql = sql + "SELECT a.COLUMN_NAME FROM information_schema.key_column_usage a "
    sql = sql + "INNER JOIN information_schema.table_constraints b ON a.TABLE_NAME = b.TABLE_NAME "
    sql = sql + "WHERE a.table_name = '" + nombreTabla + "' AND b.constraint_type = 'PRIMARY KEY') "
    sql = sql + "ORDER BY ORDINAL_POSITION;"
    df = pd.read_sql(sql, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def generarNombreProcedimientoAlmacenado(nombreTabla):
    return nombreTabla + "_Delete"

def generarNombreArchivoProcedimientoAlmacenado(nombreProcimientoAlmacenado):
    return nombreProcimientoAlmacenado + ".sql"