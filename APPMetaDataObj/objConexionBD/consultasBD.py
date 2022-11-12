from objConexionBD.objetoConexion import gestionBaseDatos
from consultasSQL import obtenerConsultaSQL
from util.enumerados import tipoConsulta

class obtenerData():

    def __init__(self, nombreTabla):
        self.__nombreTabla = nombreTabla
        pass

    def metaDataClavePrincipal(self):
        dataConsulta = {}
        conexion = gestionBaseDatos(self.__nombreTabla)
        sql = obtenerConsultaSQL.consultaMetaDatos(self.__nombreTabla, tipoConsulta.SoloPK)
        dataConsulta = conexion.consultarDatosBD(sql)
        
        return dataConsulta

    def metaDataTodosCampos(self):
        dataConsulta = {}
        conexion = gestionBaseDatos(self.__nombreTabla)
        sql = obtenerConsultaSQL.consultaMetaDatos(self.__nombreTabla, tipoConsulta.TodosCampos)   
        dataConsulta = conexion.consultarDatosBD(sql)
        
        return dataConsulta

    def metaDataCamposSinClavePrincipal(self):
        dataConsulta = {}
        conexion = gestionBaseDatos(self.__nombreTabla)
        sql = obtenerConsultaSQL.consultaMetaDatos(self.__nombreTabla, tipoConsulta.CamposSinPK)  
        dataConsulta = conexion.consultarDatosBD(sql)
        
        return dataConsulta