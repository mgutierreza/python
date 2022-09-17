import pyodbc as pyo
import pandas as pd

def obtenerMetaDataCampos(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT COLUMN_NAME nombreCampo, upper(DATA_TYPE) tipoDato, isnull(CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo "
    sql = sql + "FROM information_schema.columns "
    sql = sql + "WHERE table_name = '" + nombreTabla + "' "
    sql = sql + "ORDER BY ORDINAL_POSITION;"
    df = pd.read_sql(sql, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataClavePrincipal(nombreTabla):

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