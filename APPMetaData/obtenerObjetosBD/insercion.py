import pyodbc as pyo
import pandas as pd
from os import remove

def crearSPInserciónDatos(nombreTabla):
    procedimientoAlmacenado = ""
    nombreProcedimientoAlmacenado = generarNombreProcedimientoAlmacenado(nombreTabla)
    nombreArchivoProcedimientoAlmacenado = generarNombreArchivoProcedimientoAlmacenado(nombreProcedimientoAlmacenado)
    cabeceraProcedimientoAlmacenado = generarCabeceraProcedimientoAlmacenado(nombreTabla)
    cuerpoProcedimientoAlmacenado = generarCuerpoProcedimientoAlmacenado(nombreTabla)
    
    procedimientoAlmacenado = cabeceraProcedimientoAlmacenado + cuerpoProcedimientoAlmacenado
    
    #remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivoProcedimientoAlmacenado,'w')
    f.write(procedimientoAlmacenado)
    f.close()

    return 

def generarCuerpoProcedimientoAlmacenado(nombreTabla):
    cuerpoProcedimientoAlmacenado = ""
    inicioComandoInsercion = "\t\t\t\tINSERT INTO dbo." + nombreTabla + "(\n"
    camposComandoInsercion = ""
    inicioValoresInsercion = "\t\t\t\t\t\t\t\t)\n\t\t\t\tVALUES\n\t\t\t\t\t\t\t\t(\n"
    valoresComandoInsercion = ""
    finValoresInsercion = "\t\t\t\t\t\t\t\t)\n"
    retornoProcedimientoAlmacenado = ""
    finProcedimientoAlmacenado = "\nEND"
    
    df = identificarCampos(nombreTabla)

    for i in df.index:
        camposComandoInsercion = camposComandoInsercion + "\t\t\t\t\t\t\t\t\t\t" + nombreTabla + "." + df["nombreCampo"][i] + ",\n"
        if ((df["tipoDato"][i] == 'DATETIME') and ("Registro" in df["nombreCampo"][i])):
            valoresComandoInsercion = valoresComandoInsercion + "\t\t\t\t\t\t\t\t\t\tGETDATE(),\n"
        else:
            valoresComandoInsercion = valoresComandoInsercion + "\t\t\t\t\t\t\t\t\t\t@" + df["nombreCampo"][i] + ",\n"

    last_char_index = camposComandoInsercion.rfind(",")
    camposComandoInsercion = camposComandoInsercion[:last_char_index] + "\n"

    last_char_index = valoresComandoInsercion.rfind(",")
    valoresComandoInsercion = valoresComandoInsercion[:last_char_index] + "\n"

    df = identificarClavePrimaria(nombreTabla)

    for i in df.index:
        retornoProcedimientoAlmacenado = retornoProcedimientoAlmacenado + "\t\t\t\tSET @"+ df["nombreCampo"][i] + "\t=\t@@IDENTITY\n"
    
    cuerpoProcedimientoAlmacenado = inicioComandoInsercion + camposComandoInsercion + inicioValoresInsercion
    cuerpoProcedimientoAlmacenado = cuerpoProcedimientoAlmacenado + valoresComandoInsercion + finValoresInsercion
    cuerpoProcedimientoAlmacenado = cuerpoProcedimientoAlmacenado + retornoProcedimientoAlmacenado + finProcedimientoAlmacenado

    return cuerpoProcedimientoAlmacenado

def generarCabeceraProcedimientoAlmacenado(nombreTabla):
    CabeceraProcedimientoAlmacenado = ""
    libreriaProcedimientoAlmacenado = "SET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\n\n"
    inicioCabeceraProcedimientoAlmacenado = "CREATE PROCEDURE dbo." + generarNombreProcedimientoAlmacenado(nombreTabla) + "\n(\n"
    finCabeceraProcedimientoAlmacenado = ")\nAS\nBEGIN\n"
    parametrosClavePrincipal = ""
    parametrosProcedimientoAlmacenado = ""
    
    df = identificarClavePrimaria(nombreTabla)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME'):
            parametrosClavePrincipal = parametrosClavePrincipal + "\t\t@"+ df["nombreCampo"][i] + "\t\t\t\t\t\t\t\t\t\t" + df["tipoDato"][i] + " OUTPUT,\n"
        else:
            parametrosClavePrincipal = parametrosClavePrincipal + "\t\t@"+ df["nombreCampo"][i] + "\t\t\t\t\t\t\t\t\t\t" + df["tipoDato"][i] + "(" + (df["tamanhoCampo"][i]).astype(str) + ") OUTPUT,\n"

    last_char_index = parametrosClavePrincipal.rfind(",")
    parametrosClavePrincipal = parametrosClavePrincipal[:last_char_index] + "\n"

    df = identificarCampos(nombreTabla)
    for i in df.index:
        if (df["tipoDato"][i] == 'INT' or df["tipoDato"][i] == 'DATE' or df["tipoDato"][i] == 'DATETIME'):
            parametrosProcedimientoAlmacenado = parametrosProcedimientoAlmacenado + "\t\t@"+ df["nombreCampo"][i] + "\t\t\t\t\t\t\t\t\t\t" + df["tipoDato"][i] + ",\n"
        else:
            parametrosProcedimientoAlmacenado = parametrosProcedimientoAlmacenado + "\t\t@"+ df["nombreCampo"][i] + "\t\t\t\t\t\t\t\t\t\t" + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i].astype(str) + "),\n"

    last_char_index = parametrosProcedimientoAlmacenado.rfind(",")
    parametrosProcedimientoAlmacenado = parametrosProcedimientoAlmacenado[:last_char_index] + "\n"

    CabeceraProcedimientoAlmacenado = libreriaProcedimientoAlmacenado + inicioCabeceraProcedimientoAlmacenado + parametrosClavePrincipal
    CabeceraProcedimientoAlmacenado = CabeceraProcedimientoAlmacenado + parametrosProcedimientoAlmacenado + finCabeceraProcedimientoAlmacenado

    return CabeceraProcedimientoAlmacenado

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

    numeroCampos = len(df.index)
    rangoMenor = numeroCampos - 3
    rangoMayor = numeroCampos
    df1 = df.drop(range(rangoMenor,rangoMayor))
    numeroCampos = len(df1.index)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df1
    
def generarNombreProcedimientoAlmacenado(nombreTabla):
    return nombreTabla + "_Insert"

def generarNombreArchivoProcedimientoAlmacenado(nombreProcimientoAlmacenado):
    return nombreProcimientoAlmacenado + ".sql"