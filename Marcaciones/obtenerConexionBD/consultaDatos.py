import pyodbc as pyo
import pandas as pd
from utilitarios import enumerados

conexionBD = None

def obtenerMetaDataTodosCampos(nombreTabla):

    df = realizarConsulta(nombreTabla, enumerados.tipoConsulta.TodosCampos)

    return df

def obtenerMetaDataClavePrincipal(nombreTabla):

    df = realizarConsulta(nombreTabla, enumerados.tipoConsulta.SoloPK)

    return df

def obtenerMetaDataClaveForanea(nombreTabla):

    df = realizarConsulta(nombreTabla, enumerados.tipoConsulta.SoloFK)

    return df

def obtenerMetaDataCamposSinClavePrincipal(nombreTabla):

    df = realizarConsulta(nombreTabla, enumerados.tipoConsulta.CamposSinPK)

    return df

def obtenerMetaDataClaves(nombreTabla):

    df = realizarConsulta(nombreTabla, enumerados.tipoConsulta.SoloPKFK)

    return df

def obtenerMetaDataFK(nombreTabla):
    global conexionBD

    conexionBD = __abrirConexionBD()
    consultaSQL = __consultaMetaDatosFK(nombreTabla)
    df = pd.read_sql(consultaSQL, conexionBD)
    __cerrarConexionBD()

    return df

def realizarConsulta(nombreTabla, tipoConsulta):
    global conexionBD

    conexionBD = __abrirConexionBD()
    consultaSQL = __consultaMetaDatos(nombreTabla, tipoConsulta)
    df = pd.read_sql(consultaSQL, conexionBD)
    __cerrarConexionBD()

    return df

def __consultaMetaDatos(nombreTabla, tipoConsulta):
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
    
    if (tipoConsulta == enumerados.tipoConsulta.SoloPK):
        sql += "AND c.CONSTRAINT_TYPE = 'PRIMARY KEY' "        
    elif(tipoConsulta == enumerados.tipoConsulta.CamposSinPK):
        sql += "AND ISNULL(c.CONSTRAINT_TYPE,'X') NOT IN ('PRIMARY KEY') "
    elif(tipoConsulta == enumerados.tipoConsulta.SoloPKFK):
        sql += "AND c.CONSTRAINT_TYPE IN ('PRIMARY KEY','FOREIGN KEY') "    
    elif(tipoConsulta == enumerados.tipoConsulta.SoloFK):
        sql += "AND c.CONSTRAINT_TYPE IN ('FOREIGN KEY') "            

    sql += "ORDER BY a.ORDINAL_POSITION "    				 

    return sql

def __consultaMetaDatosFK(nombreTabla):
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

def __abrirConexionBD():
    cadenaConexion = ""
    global conexionBD

    if (conexionBD is None):
        cadenaConexion = (
            r"Driver={SQL SERVER};Server=132.16.0.49;Database=BDDatos;UID=Prueba;PWD=Prueba"
            )
        conexionBD = pyo.connect(cadenaConexion)

    return conexionBD

def __cerrarConexionBD():
    global conexionBD

    if (conexionBD is not None):
        conexionBD.close()
        conexionBD = None

    return 