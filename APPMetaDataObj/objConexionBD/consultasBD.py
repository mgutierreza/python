from objConexionBD.objetoConexion import gestionBaseDatos

class obtenerData():

    def __init__(self, nombreTabla):
        self.__nombreTabla = nombreTabla
        pass

    def metaDataClavePrincipal(self):
        dataConsulta = {}
        conexion = gestionBaseDatos(self.__nombreTabla)

        sql = "SELECT b.COLUMN_NAME nombreCampo, UPPER(c.DATA_TYPE) tipoDato, ISNULL(c.CHARACTER_MAXIMUM_LENGTH,0) tamanhoCampo "
        sql = sql + "FROM information_schema.table_constraints a, information_schema.key_column_usage b, information_schema.columns c "
        sql = sql + "WHERE a.table_name = '" + self.__nombreTabla + "' "
        sql = sql + "AND a.table_name = b.table_name "
        sql = sql + "AND a.table_schema = b.TABLE_SCHEMA "
        sql = sql + "AND a.constraint_name = b.constraint_name "
        sql = sql + "AND b.COLUMN_NAME = c.COLUMN_NAME AND b.TABLE_NAME = c.TABLE_NAME "
        sql = sql + "AND a.CONSTRAINT_TYPE = 'PRIMARY KEY' "
        sql = sql + "ORDER BY c.ORDINAL_POSITION"        

        dataConsulta = conexion.consultarDatosBD(sql)
        
        return dataConsulta