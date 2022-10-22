import pyodbc as pyo
import pandas as pd
from utilitarios import generarRutaArchivo, generarNombreArchivo, generarArchivo, generarExtensionArchivo
from utilitarios import enumerados
from obtenerConexionBD import consultaDatos
from utilitarios import util

TAB = "\t"
ENTER = "\n"


def generarJSONInsercion(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.JSON)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.insert)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.JSON)
    contenidoArchivo = crearJSONInsercion(nombreTabla)
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return
'''
def generarJSONActualizacion(nombreTabla):
    rutaArchivo = generarRutaArchivo(nombreTabla, enumerados.tipoObjeto.JSON)
    nombreArchivo = generarNombreArchivo(nombreTabla, enumerados.claseObjeto.update)
    extensionArchivo = generarExtensionArchivo(enumerados.tipoObjeto.JSON)
    contenidoArchivo = crearJSONActualizacion(nombreTabla)
    generarArchivo(rutaArchivo, nombreArchivo + extensionArchivo, contenidoArchivo)

    return'''

def crearJSONInsercion(nombreTabla):
    json = ""
    valor = ""

    df = consultaDatos.obtenerMetaDataTodosCampos(nombreTabla)

    json += "{" + ENTER
    
    for i in df.index:
        valor = generarValorAleatorio(df["nombreCampo"][i], df["tipoDatoBD"][i], df["tipoCampo"][i])
        if (df["tipoDatoBD"][i] == 'INT' or df["tipoDatoBD"][i] == 'BIGINT' or df["tipoDatoBD"][i] == 'DECIMAL'):
            json += TAB + "\"" + df["nombreCampo"][i] + "\" : " + valor + "," + ENTER
        else:
            json += TAB + "\"" + df["nombreCampo"][i] + "\" : \"" + valor + "\"," + ENTER

    json += "}" + ENTER

    return json

'''
def crearJSONActualizacion(nombreTabla):
    json = ""

    return json
'''

def generarValorAleatorio(nombreCampo, tipoDatoBD, tipoCampo):
    nuevoValor = ""
    tipoDatoGeneral = ""

    
    if (tipoDatoBD == 'VARCHAR' or tipoDatoBD == 'CHAR' or tipoDatoBD == 'NCHAR' or tipoDatoBD == 'NVARCHAR'):
        tipoDatoGeneral = "texto"
    if (tipoDatoBD == 'INT' or tipoDatoBD == 'BIGINT' or tipoDatoBD == 'TINYINT'):
        tipoDatoGeneral = "entero"
    if (tipoDatoBD == 'DECIMAL' or tipoDatoBD == 'NUMERIC' or tipoDatoBD == 'MONEY'):
        tipoDatoGeneral = "decimal"
    if (tipoDatoBD == 'DATETIME'):
        tipoDatoGeneral = "fecha"
    
    if(tipoCampo == 'PRIMARY KEY'):
        valor = "0"

    if((tipoDatoGeneral == 'fecha') and ('Registro','Upd' in (nombreCampo))):
        valor = "2022-09-30T02:17:07.613Z"
    
    if((tipoDatoGeneral == 'fecha') and ('Registro','Upd' not in (nombreCampo))):
        valor = "2022-08-30T02:17:07.613Z"
 
    if(tipoCampo == 'CAMPO' and tipoDatoGeneral == 'entero'):
        valor = "1"

    if((tipoDatoGeneral == 'texto') and ('Registro','Upd' in (nombreCampo)) and  ('Usu' in (nombreCampo))):
        valor = "1009121972"
    
    if((tipoDatoGeneral == 'texto') and ('Registro','Upd' in (nombreCampo)) and  ('Host' in (nombreCampo))):
        valor = "127.0.0.1"
    
    if(tipoDatoGeneral == 'decimal'):
        valor = "11.22"
  
    return valor
