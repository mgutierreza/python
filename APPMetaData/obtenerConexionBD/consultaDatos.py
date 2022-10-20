import pyodbc as pyo
import pandas as pd

def obtenerMetaDataTodosCampos(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT a.COLUMN_NAME nombreCampo, upper(a.DATA_TYPE) tipoDato, isnull(a.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo, ISNULL(c.CONSTRAINT_TYPE, 'CAMPO') tipoCampo "
    sql = sql + "FROM information_schema.columns a "
    sql = sql + "LEFT JOIN information_schema.key_column_usage b ON a.COLUMN_NAME = b.COLUMN_NAME AND a.TABLE_NAME = b.TABLE_NAME AND a.TABLE_SCHEMA = b.TABLE_SCHEMA "
    sql = sql + "LEFT JOIN information_schema.table_constraints c ON b.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND b.TABLE_NAME = c.TABLE_NAME AND b.TABLE_SCHEMA = c.TABLE_SCHEMA "
    sql = sql + "WHERE a.table_name = '" + nombreTabla + "' "
    sql = sql + "ORDER BY a.ORDINAL_POSITION"
    df = pd.read_sql(sql, conexionAzure)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            df["tipoDato"][i] = 'Int32'
        elif (df["tipoDato"][i] == 'BIGINT'):
            df["tipoDato"][i] = 'Int64'
        elif (df["tipoDato"][i] == 'VARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'CHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NVARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'DECIMAL'):
            df["tipoDato"][i] = 'Decimal'
        else:
            df["tipoDato"][i] = 'DateTime'

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
    sql = sql + "AND a.CONSTRAINT_TYPE = 'PRIMARY KEY' "
    sql = sql + "ORDER BY c.ORDINAL_POSITION"
    
    df = pd.read_sql(sql, conexionAzure)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            df["tipoDato"][i] = 'Int32'
        elif (df["tipoDato"][i] == 'BIGINT'):
            df["tipoDato"][i] = 'Int64'
        elif (df["tipoDato"][i] == 'VARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'CHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NVARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'DECIMAL'):
            df["tipoDato"][i] = 'Decimal'
        else:
            df["tipoDato"][i] = 'DateTime'

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataCamposSinClavePrincipal(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT a.COLUMN_NAME nombreCampo, upper(a.DATA_TYPE) tipoDato, isnull(a.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo "
    sql = sql + "FROM information_schema.columns a "
    sql = sql + "LEFT JOIN information_schema.key_column_usage b ON a.COLUMN_NAME = b.COLUMN_NAME AND a.TABLE_NAME = b.TABLE_NAME AND a.TABLE_SCHEMA = b.TABLE_SCHEMA "
    sql = sql + "LEFT JOIN information_schema.table_constraints c ON b.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND b.TABLE_NAME = c.TABLE_NAME AND b.TABLE_SCHEMA = c.TABLE_SCHEMA "
    sql = sql + "WHERE a.table_name = '" + nombreTabla + "' "
    sql = sql + "AND ISNULL(c.CONSTRAINT_TYPE,'X') NOT IN ('PRIMARY KEY') "
    sql = sql + "ORDER BY a.ORDINAL_POSITION"
    
    df = pd.read_sql(sql, conexionAzure)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            df["tipoDato"][i] = 'Int32'
        elif (df["tipoDato"][i] == 'BIGINT'):
            df["tipoDato"][i] = 'Int64'
        elif (df["tipoDato"][i] == 'VARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'CHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NVARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'DECIMAL'):
            df["tipoDato"][i] = 'Decimal'
        else:
            df["tipoDato"][i] = 'DateTime'    

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataClaves(nombreTabla):

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
    sql = sql + "AND a.CONSTRAINT_TYPE IS NOT NULL "
    sql = sql + "ORDER BY c.ORDINAL_POSITION"
    
    df = pd.read_sql(sql, conexionAzure)

    for i in df.index:
        if (df["tipoDato"][i] == 'INT'):
            df["tipoDato"][i] = 'Int32'
        elif (df["tipoDato"][i] == 'BIGINT'):
            df["tipoDato"][i] = 'Int64'
        elif (df["tipoDato"][i] == 'VARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'CHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'NVARCHAR'):
            df["tipoDato"][i] = 'String'
        elif (df["tipoDato"][i] == 'DECIMAL'):
            df["tipoDato"][i] = 'Decimal'
        else:
            df["tipoDato"][i] = 'DateTime'

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataTodosCamposBD(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT a.COLUMN_NAME nombreCampo, upper(a.DATA_TYPE) tipoDato, isnull(a.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo, ISNULL(c.CONSTRAINT_TYPE, 'CAMPO') tipoCampo "
    sql = sql + "FROM information_schema.columns a "
    sql = sql + "LEFT JOIN information_schema.key_column_usage b ON a.COLUMN_NAME = b.COLUMN_NAME AND a.TABLE_NAME = b.TABLE_NAME AND a.TABLE_SCHEMA = b.TABLE_SCHEMA "
    sql = sql + "LEFT JOIN information_schema.table_constraints c ON b.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND b.TABLE_NAME = c.TABLE_NAME AND b.TABLE_SCHEMA = c.TABLE_SCHEMA "
    sql = sql + "WHERE a.table_name = '" + nombreTabla + "' "
    sql = sql + "ORDER BY a.ORDINAL_POSITION"
    df = pd.read_sql(sql, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataClavePrincipalBD(nombreTabla):

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
    sql = sql + "AND a.CONSTRAINT_TYPE = 'PRIMARY KEY' "
    sql = sql + "ORDER BY c.ORDINAL_POSITION"
    
    df = pd.read_sql(sql, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df

def obtenerMetaDataCamposSinClavePrincipalBD(nombreTabla):

    conexionAzure = (
        r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
    
    conexionAzure = pyo.connect(conexionAzure)
    print('Conexión Abierta')
    
    sql = "SELECT a.COLUMN_NAME nombreCampo, upper(a.DATA_TYPE) tipoDato, isnull(a.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo "
    sql = sql + "FROM information_schema.columns a "
    sql = sql + "LEFT JOIN information_schema.key_column_usage b ON a.COLUMN_NAME = b.COLUMN_NAME AND a.TABLE_NAME = b.TABLE_NAME AND a.TABLE_SCHEMA = b.TABLE_SCHEMA "
    sql = sql + "LEFT JOIN information_schema.table_constraints c ON b.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND b.TABLE_NAME = c.TABLE_NAME AND b.TABLE_SCHEMA = c.TABLE_SCHEMA "
    sql = sql + "WHERE a.table_name = '" + nombreTabla + "' "
    sql = sql + "AND ISNULL(c.CONSTRAINT_TYPE,'X') NOT IN ('PRIMARY KEY') "
    sql = sql + "ORDER BY a.ORDINAL_POSITION"
    
    df = pd.read_sql(sql, conexionAzure)

    conexionAzure.close()
    print('Conexión Cerrada')

    return df