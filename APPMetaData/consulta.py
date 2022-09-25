import pyodbc as pyo
import pandas as pd
from os import remove

def generarNombreProcedimientoAlmacenado(nombreTabla):
    return nombreTabla + "_Get"


def generarNombreArchivoProcedimientoAlmacenado(nombreProcimientoAlmacenado):
    return nombreProcimientoAlmacenado + ".sql"


def generarDiccionarioMetaDataClavesPrimarias(nombreTabla):
    metaDataEstructuraCampos = {
        "nombreCampo": [],
        "tipoDato": [],
        "tamanhoCampo": []
    }

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql2 = "SELECT b.COLUMN_NAME nombreCampo, UPPER(c.DATA_TYPE) tipoDato, c.CHARACTER_MAXIMUM_LENGTH tamanhoCampo "
    sql2 = sql2 + "FROM information_schema.table_constraints a, information_schema.key_column_usage b, information_schema.columns c "
    sql2 = sql2 + "WHERE a.table_name = '" + nombreTabla +"' "
    sql2 = sql2 + "AND a.table_name = b.table_name "
    sql2 = sql2 + "AND a.table_schema = b.TABLE_SCHEMA "
    sql2 = sql2 + "AND a.constraint_name = b.constraint_name "
    sql2 = sql2 + "AND b.COLUMN_NAME = c.COLUMN_NAME AND b.TABLE_NAME = c.TABLE_NAME "
    sql2 = sql2 + "AND a.CONSTRAINT_TYPE = 'PRIMARY KEY'"
    df = pd.read_sql(sql2, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df
    
def generarCabeceraProcedimientoAlmacenado(nombreTabla):
    libreriaProcedimientoAlmacenado = "SET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\n\n"
    cabeceraProcedimientoAlmacenado = ""
    parametrosEntradaProcedimientoAlmacenado = ""

    df = generarDiccionarioMetaDataClavesPrimarias(nombreTabla)
    numeroRegistroDiccionario = len(df)

    for i in df.index:
        if (numeroRegistroDiccionario > 1):
            if (df["tipoDato"][i] == 'INT'):
                parametrosEntradaProcedimientoAlmacenado = parametrosEntradaProcedimientoAlmacenado + "\t\t@"+ df["nombreCampo"][i] + "\t" + df["tipoDato"][i] + " = 0,"
            else:
                parametrosEntradaProcedimientoAlmacenado = parametrosEntradaProcedimientoAlmacenado + "\t\t@"+ df["nombreCampo"][i] + "\t" + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i] + ") = 'null',"
        else:
            if (df["tipoDato"][i] == 'INT'):
                parametrosEntradaProcedimientoAlmacenado = "\t\t@"+ df["nombreCampo"][i] + "\t" + df["tipoDato"][i] + " = 0,"
            else:
                parametrosEntradaProcedimientoAlmacenado = "\t\t@"+ df["nombreCampo"][i] + "\t" + df["tipoDato"][i] + "(" + df["tamanhoCampo"][i] + ") = 'null',"
    
    last_char_index = parametrosEntradaProcedimientoAlmacenado.rfind(",")
    parametrosEntradaProcedimientoAlmacenado = parametrosEntradaProcedimientoAlmacenado[:last_char_index] + "\n"
    cabeceraProcedimientoAlmacenado = libreriaProcedimientoAlmacenado + "CREATE PROCEDURE dbo." + generarNombreProcedimientoAlmacenado(nombreTabla) + "\n(\n" 
    cabeceraProcedimientoAlmacenado = cabeceraProcedimientoAlmacenado + parametrosEntradaProcedimientoAlmacenado + ")\nAS\n\tBEGIN\n"
    
    return cabeceraProcedimientoAlmacenado

def generarCondicionalProcedimientoAlmacenado(nombreTabla):
    df = generarDiccionarioMetaDataClavesPrimarias(nombreTabla)
    estructuraControlSQLIF = ""
    
    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            estructuraControlSQLIF = "\t\tIF (@"+ df["nombreCampo"][i] +" > 0)\n"
        else:
            estructuraControlSQLIF = "\t\tIF (@"+ df["nombreCampo"][i] +" = 'null')\n"

    return estructuraControlSQLIF
           

def generarDiccionarioMetaDataCampos(nombreTabla):
    metaDataEstructuraCampos = {
        "nombreCampo": []
    }

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT COLUMN_NAME nombreCampo FROM information_schema.columns WHERE table_name = '"+ nombreTabla +"' ORDER BY ORDINAL_POSITION;"
    df = pd.read_sql(sql, conexionAzure)
    
    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def generarConsultaProcedimientoAlmacenado(nombreTabla):
    
    df = generarDiccionarioMetaDataCampos(nombreTabla)
    lineaCodigoProcedimientoAlmacenado = ""
    consultaProcedimientoAlmacenado = ""
    
    for i in df.index:
        lineaCodigoProcedimientoAlmacenado = lineaCodigoProcedimientoAlmacenado + '\t\t\t\t\t' + nombreTabla + '.' + df["nombreCampo"][i] + ",\n"
    
    last_char_index = lineaCodigoProcedimientoAlmacenado.rfind(",")
    lineaCodigoProcedimientoAlmacenado = lineaCodigoProcedimientoAlmacenado[:last_char_index] + "\n"
    consultaProcedimientoAlmacenado = "\t\t\t\tSELECT\n" + lineaCodigoProcedimientoAlmacenado 
    consultaProcedimientoAlmacenado = consultaProcedimientoAlmacenado + "\t\t\t\tFROM " + "dbo." + nombreTabla + " WITH(NOLOCK)\n"

    return consultaProcedimientoAlmacenado


def crearSPConsultaDatos(nombreTabla):
    

    nombreProcedimientoAlmacenado = generarNombreProcedimientoAlmacenado(nombreTabla)
    nombreArchivoProcedimientoAlmacenado = generarNombreArchivoProcedimientoAlmacenado(nombreProcedimientoAlmacenado)

    cabeceraProcedimientoAlmacenado = generarCabeceraProcedimientoAlmacenado(nombreTabla)
    condicionalProcedimientoAlmacenado = generarCondicionalProcedimientoAlmacenado(nombreTabla)
    consultaProcedimientoAlmacenado = generarConsultaProcedimientoAlmacenado(nombreTabla)

    comandoInicioEstructura = "\t\t\tBEGIN\n"
    comandoFinEstructura = "\t\t\tEND\n"
    estructuraControlSQLELSE = "\t\tELSE\n"  
    comandoFinProcedimientoAlmacenado = "\tEND"

    procedimientoAlmacenado = cabeceraProcedimientoAlmacenado + condicionalProcedimientoAlmacenado + comandoInicioEstructura
    procedimientoAlmacenado = procedimientoAlmacenado + consultaProcedimientoAlmacenado + comandoFinEstructura + estructuraControlSQLELSE 
    procedimientoAlmacenado = procedimientoAlmacenado + comandoInicioEstructura + consultaProcedimientoAlmacenado + comandoFinEstructura 
    procedimientoAlmacenado = procedimientoAlmacenado + comandoFinProcedimientoAlmacenado
    
    remove(nombreArchivoProcedimientoAlmacenado)
    f = open (nombreArchivoProcedimientoAlmacenado,'w')
    f.write(procedimientoAlmacenado)
    f.close()
  