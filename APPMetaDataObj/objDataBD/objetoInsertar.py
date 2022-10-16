from util.utilitario import gestionArchivos
from objConexionBD.consultasBD import obtenerData

class objetoProcedimientoInsertar():

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreObjeto = ''
        self.TAB = '\t'
        self.ENTER = '\n'
        self.ESPACIO = ' '

    def generarArchivo(self):
        nuevoArchivo = gestionArchivos(self.__nombreTabla, self.__claseObjeto)
        self.__nombreObjeto = nuevoArchivo.generarNombreArchivo()
        contenidoClase = self.__generarProcedimientoAlmacenado()
        nuevoArchivo.generarArchivo(contenidoClase)
        return

    def __generarProcedimientoAlmacenado(self):
        procedimientoAlmacenado = ""
        procedimientoAlmacenado += self.__generarLibreriasProcedimientoAlmacenado()
        procedimientoAlmacenado += self.__generarCabeceraProcedimientoAlmacenado()
        procedimientoAlmacenado += self.__generarCuerpoProcedimientoAlmacenado()        
        
        return procedimientoAlmacenado
    
    def __generarLibreriasProcedimientoAlmacenado(self):
        libreriasProcedimientoAlmacenado = ""
        libreriasProcedimientoAlmacenado += "SET ANSI_NULLS ON" + self.ENTER 
        libreriasProcedimientoAlmacenado += "GO" + self.ENTER 
        libreriasProcedimientoAlmacenado += "SET QUOTED_IDENTIFIER ON" + self.ENTER
        libreriasProcedimientoAlmacenado += "GO" + 2*self.ENTER

        return libreriasProcedimientoAlmacenado
    
    def __generarCabeceraProcedimientoAlmacenado(self):
        cabeceraProcedimientoAlmacenado = ""
        cabeceraProcedimientoAlmacenado += "CREATE PROCEDURE dbo." + self.__nombreObjeto + self.ENTER
        cabeceraProcedimientoAlmacenado += "(" + self.ENTER
        cabeceraProcedimientoAlmacenado += self.__generarParametrosEntradaProcedimientoAlmacenado()      
        cabeceraProcedimientoAlmacenado += ")" + self.ENTER 
        cabeceraProcedimientoAlmacenado += "AS" + self.ENTER
        cabeceraProcedimientoAlmacenado += "BEGIN" + self.ENTER
        
        return cabeceraProcedimientoAlmacenado

    def __generarCuerpoProcedimientoAlmacenado(self):
        cuerpoProcedimientoAlmacenado = ""
        cuerpoProcedimientoAlmacenado += 4*self.TAB + "UPDATE dbo." + self.__nombreTabla + self.ENTER
        cuerpoProcedimientoAlmacenado += 4*self.TAB + "SET" + self.ENTER
        cuerpoProcedimientoAlmacenado += self.__generarCamposParaActualizar()
        cuerpoProcedimientoAlmacenado +=  4*self.TAB + "WHERE" + self.ENTER
        cuerpoProcedimientoAlmacenado += self.__generarCamposParaFiltro()
        cuerpoProcedimientoAlmacenado += "END" + self.ENTER

        return cuerpoProcedimientoAlmacenado
    
    def __generarCamposParaActualizar(self):
        camposParaActualizar = ""
        espacioEstandar = 30

        dictData = self.__obtenerParametrosParaActualizacion()

        for valor in dictData:
            espacioCampo = len(valor["nombreCampo"])
            espacioFaltante = espacioEstandar - espacioCampo        
            if ((valor["tipoDato"] == 'DATETIME') and ("Update" in valor["nombreCampo"])):
                camposParaActualizar += 5*self.TAB + "dbo." + self.__nombreTabla + "." + valor["nombreCampo"] + espacioFaltante*self.ESPACIO + "=" + 2*self.TAB + "GETDATE()," + self.ENTER
            else:
                camposParaActualizar += 5*self.TAB + "dbo." + self.__nombreTabla + "." + valor["nombreCampo"] + espacioFaltante*self.ESPACIO + "=" + 2*self.TAB + "@" + valor["nombreCampo"] + "," + self.ENTER
        
        camposParaActualizar = gestionArchivos.extraerUltimoCaracter(camposParaActualizar) + self.ENTER

        return camposParaActualizar    

    def __generarParametrosEntradaProcedimientoAlmacenado(self):
        parametrosEntrada = ""
        espacioEstandar = 30

        dictData = self.__obtenerParametrosParaActualizacion()
        for valor in dictData:
            if ((valor["tipoDato"] == 'DATETIME') and ("Upd" in valor["nombreCampo"])):
                parametrosEntrada += ""
            else:
                espacioCampo = len(valor["nombreCampo"])
                espacioFaltante = espacioEstandar - espacioCampo
                if (valor["tipoDato"] == 'INT' or valor["tipoDato"] == 'DATE' or valor["tipoDato"] == 'DATETIME'):
                    parametrosEntrada += 5*self.TAB + "@"+ valor["nombreCampo"] + espacioFaltante*self.ESPACIO + 2*self.TAB + valor["tipoDato"] + "," + self.ENTER
                else:
                    parametrosEntrada += 5*self.TAB + "@"+ valor["nombreCampo"] + espacioFaltante*self.ESPACIO + 2*self.TAB + valor["tipoDato"] + "(" + valor["tamanhoCampo"].astype(str) + ")," + self.ENTER

        parametrosEntrada = gestionArchivos.extraerUltimoCaracter(parametrosEntrada) + self.ENTER

        return parametrosEntrada
    
    def __generarCamposParaFiltro(self):
        camposParaFiltro = ""
        espacioEstandar = 30

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            espacioCampo = len(valor["nombreCampo"])
            espacioFaltante = espacioEstandar - espacioCampo
            camposParaFiltro += 5*self.TAB + "dbo." + self.__nombreTabla + "." + valor["nombreCampo"] + espacioFaltante*self.ESPACIO + " = " + 2*self.TAB + "@" + valor["nombreCampo"] + self.ENTER
        
        return camposParaFiltro

    def __obtenerParametrosParaActualizacion(self):

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataTodosCampos()

        numeroCampos = len(dictData)
        x = numeroCampos - 4
        y = numeroCampos - 5
        z = numeroCampos - 6
        dictData.pop(x)
        dictData.pop(y)
        dictData.pop(z)

        return dictData        