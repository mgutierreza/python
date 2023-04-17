import cx_Oracle
import pandas as pd

cursor = None
dataCarnetIdentificacion = []

def getConexionBD():
    conexion = cx_Oracle.connect(user="UC_MGUTIERREZA",password="pC9Jblu5",dsn="172.17.23.42:1531/bdpr11g4")
    #conexion = cx_Oracle.connect(user="UM_MGUTIERREZ",password="R4354%&$t",dsn="172.17.23.9:1530/bdqa11g4")
    cursor = conexion.cursor()
    return cursor
    
def getCarnetIdentificacion(usuario):
    carnetIdentificacion = '&&&&&'
    global dataCarnetIdentificacion

    if not dataCarnetIdentificacion:
        dataCarnetIdentificacion = getDataCarnetIdentificacion()
    
    for valor in dataCarnetIdentificacion:
        if valor['CODIGOUSUARIO'] == usuario:
            carnetIdentificacion = str(valor['CODIGOCARNET'])
            break

    return carnetIdentificacion

def getDataCarnetIdentificacion():
    global cursor

    script = "SELECT pe.codigousuario, ci.codigocarnet "
    script += "FROM sgcoresys.personamast pe "
    script += "INNER JOIN sgcoresys.as_carnetidentificacion ci ON pe.persona = ci.empleado "
    script += "WHERE ci.estado = \'A\' "
    script += "AND pe.codigousuario IS NOT NULL "

    if not cursor:
        cursor = getConexionBD()

    cursor.execute(script)
    filasConsulta = cursor.fetchall()
    columnasConsulta = [column[0] for column in cursor.description]

    for filaConsulta in filasConsulta:
        dataCarnetIdentificacion.append(dict(zip(columnasConsulta, filaConsulta)))

    cursor.close()
    
    return dataCarnetIdentificacion
