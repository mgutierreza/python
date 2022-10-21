import pyodbc as pyo
import pandas as pd
from utilitarios import enumerados

def obtenerMetaDataTodosCampos(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    consultaSQL = consultaMetaDatos(nombreTabla, enumerados.tipoConsulta.TodosCampos)
    df = pd.read_sql(consultaSQL, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataClavePrincipal(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    consultaSQL = consultaMetaDatos(nombreTabla, enumerados.tipoConsulta.SoloPK)
    df = pd.read_sql(consultaSQL, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataCamposSinClavePrincipal(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    consultaSQL = consultaMetaDatos(nombreTabla, enumerados.tipoConsulta.CamposSinPK)
    df = pd.read_sql(consultaSQL, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataClaves(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    consultaSQL = consultaMetaDatos(nombreTabla, enumerados.tipoConsulta.SoloPKFK)
    df = pd.read_sql(consultaSQL, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataFK(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    consultaSQL = consultaMetaDatosFK(nombreTabla)
    df = pd.read_sql(consultaSQL, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df
    
def consultaMetaDatos(nombreTabla, tipoConsulta):
    sql = ""

    sql += "SELECT "
    sql += "a.COLUMN_NAME nombreCampo, "
    sql += "UPPER(a.DATA_TYPE) tipoDatoBD, "
    sql += "ISNULL(a.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo, "
    sql += "ISNULL(c.CONSTRAINT_TYPE, 'CAMPO') tipoCampo, "
    sql += "CASE a.DATA_TYPE "
    sql += "WHEN 'BIGINT' THEN 'Int64' "
    sql += "WHEN 'INT' THEN 'Int32' "
    sql += "WHEN 'VARCHAR' THEN 'String' "
    sql += "WHEN 'CHAR' THEN 'String' "
    sql += "WHEN 'NVARCHAR' THEN 'String' "
    sql += "WHEN 'TINYINT' THEN 'Byte' "
    sql += "WHEN 'SMALLINT' THEN 'Int16' "
    sql += "WHEN 'NCHAR' THEN 'String' "
    sql += "WHEN 'DECIMAL' THEN 'Decimal' "
    sql += "WHEN 'MONEY' THEN 'Decimal' "
    sql += "WHEN 'NUMERIC' THEN 'Decimal' "
    sql += "WHEN 'REAL' THEN 'Single' "
    sql += "WHEN 'FLOAT' THEN 'Double' "
    sql += "ELSE 'DateTime' "
    sql += "END tipoDatoNET "
    sql += "FROM information_schema.columns a "    
    sql += "LEFT JOIN information_schema.key_column_usage b ON a.COLUMN_NAME = b.COLUMN_NAME AND a.TABLE_NAME = b.TABLE_NAME AND a.TABLE_SCHEMA = b.TABLE_SCHEMA "    
    sql += "LEFT JOIN information_schema.table_constraints c ON b.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND b.TABLE_NAME = c.TABLE_NAME AND b.TABLE_SCHEMA = c.TABLE_SCHEMA "    
    sql += "WHERE a.table_name = '" + nombreTabla + "' "    
    
    if (tipoConsulta == tipoConsulta.SoloPK):
        sql += "AND c.CONSTRAINT_TYPE = 'PRIMARY KEY' "        
    elif(tipoConsulta == tipoConsulta.CamposSinPK):
        sql += "AND ISNULL(c.CONSTRAINT_TYPE,'X') NOT IN ('PRIMARY KEY') "
    elif(tipoConsulta == tipoConsulta.SoloPKFK):
        sql += "AND c.CONSTRAINT_TYPE IN ('PRIMARY KEY','FOREIGN KEY') "    

    sql += "ORDER BY a.ORDINAL_POSITION "    				 

    return sql

def consultaMetaDatosFK(nombreTabla):
    sql = ""

    sql += "SELECT "
    sql += "foreign_keys.name AS nombreFK, "
    sql += "FOREIGN_KEY_TABLE.name AS tablaDestino, "
    sql += "FOREIGN_KEY_COLUMN.name AS columnaDestino, "
    sql += "REFERENCED_TABLE.name AS tablaOrigen, "
    sql += "REFERENECD_COLUMN.name AS columnaOrigen "
    sql += "FROM sys.foreign_key_columns "
    sql += "INNER JOIN sys.foreign_keys ON foreign_keys.object_id = foreign_key_columns.constraint_object_id "
    sql += "INNER JOIN sys.tables FOREIGN_KEY_TABLE ON foreign_key_columns.parent_object_id = FOREIGN_KEY_TABLE.object_id "
    sql += "INNER JOIN sys.columns as FOREIGN_KEY_COLUMN ON foreign_key_columns.parent_object_id = FOREIGN_KEY_COLUMN.object_id "
    sql += "AND foreign_key_columns.parent_column_id = FOREIGN_KEY_COLUMN.column_id "
    sql += "INNER JOIN sys.columns REFERENECD_COLUMN ON foreign_key_columns.referenced_object_id = REFERENECD_COLUMN.object_id "
    sql += "AND foreign_key_columns.referenced_column_id = REFERENECD_COLUMN.column_id "
    sql += "INNER JOIN sys.tables REFERENCED_TABLE ON REFERENCED_TABLE.object_id = foreign_key_columns.referenced_object_id "
    sql += "WHERE FOREIGN_KEY_TABLE.name = '" + nombreTabla + "' "    
    sql += "ORDER BY foreign_key_columns.constraint_column_id, FOREIGN_KEY_TABLE.name ; "    				 

    return sql