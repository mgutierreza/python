import cx_Oracle
import pandas as pd

conexion = cx_Oracle.connect(user="UM_MGUTIERREZ",password="R4354%&$t",dsn="172.17.23.9:1530/bdqa11g4")
cursor = conexion.cursor()
print("Conexion OK")

dataCarnetIdentificacion = []

def getDataCarnetIdentificacion():
    
    script = "SELECT pe.codigousuario, ci.codigocarnet "
    script += "FROM sgcoresys.personamast pe "
    script += "INNER JOIN sgcoresys.as_carnetidentificacion ci ON pe.persona = ci.empleado "
    script += "WHERE ci.estado = \'A\' "
    script += "AND pe.codigousuario IS NOT NULL "
    cursor.execute(script)
    
    filasConsulta = cursor.fetchall()
    columnasConsulta = [column[0] for column in cursor.description]

    for filaConsulta in filasConsulta:
        dataCarnetIdentificacion.append(dict(zip(columnasConsulta, filaConsulta)))

    cursor.close()        

    return dataCarnetIdentificacion

def getCarnetIdentificacion(usuario):
    carnetIdentificacion = '&&&&&'

    if not dataCarnetIdentificacion:
        dataCarnetIdentificacion = getDataCarnetIdentificacion()
    
    for valor in dataCarnetIdentificacion:
        if valor['codigousuario'] == usuario:
            carnetIdentificacion = str(valor['codigocarnet'])
            break

    return carnetIdentificacion

def getModalidad(modalidad):
    codigoModalidad = ''

    if (modalidad == 'PRESENCIAL'):
        codigoModalidad = 'PR'
    elif(modalidad == 'MIXTO REMOTO'):
        codigoModalidad = 'MR'
    elif(modalidad == 'REMOTO'):
        codigoModalidad = 'RE'
    elif(modalidad == 'MIXTO PRESENCIAL'):
        codigoModalidad = 'MP'        
    elif(modalidad == 'TELETRABAJO MIXTO REMOTO'):
        codigoModalidad = 'TR'        
    elif(modalidad == 'TELETRABAJO MIXTO PRESENCIAL'):
        codigoModalidad = 'TP'        
    elif(modalidad == 'TELETRABAJO TOTAL'):
        codigoModalidad = 'TT'
    else:
        codigoModalidad = '&&'

    return codigoModalidad

archivo_excel = pd.read_excel('d:/marcacion/Registro de asistencias del 10 de abril de 2023.xlsx')
columnas = ['Tipo de Modalidad', 'Creado', 'Integrante']
df_seleccionados = archivo_excel[columnas]

modalidades = df_seleccionados.columns[0]
marcas = df_seleccionados.columns[1]
usuarios = df_seleccionados.columns[2]

espacio = ' '
enter = "\n"
textoinicial = '099'
textofijo = '1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127'

f = open('d:/marcacion/archivoBCK_10_04_23.bck','w')

marcaBCK = ''

for index, row in df_seleccionados.iterrows():
    usuario = str(row[usuarios]).strip().replace("@onp.gob.pe","").upper()
    modalidad = str(row[modalidades]).strip().upper()
    marcaFecha = str(row[marcas]).strip()[0:10].replace("-",espacio)
    marcaHora = str(row[marcas]).strip()[11:50].replace(":",espacio)

    codigoModalidad = getModalidad(modalidad)
    carnetIdentificacion =  getCarnetIdentificacion(usuario)

    if (carnetIdentificacion != '&&&&&'):
        marcaBCK += textoinicial + espacio + marcaFecha + espacio + marcaHora + espacio + textofijo + espacio + carnetIdentificacion + espacio + modalidad + enter
    
f.write(marcaBCK)
f.close
print('fin de proceso')

cursor.close()
print("Desconectado")

#cursor.execute("SELECT * FROM sgcoresys.as_carnetidentificacion WHERE estado = \'I\'")
#rows = cursor.fetchone() # muestra un registro
#rows = cursor.fetchmany(3) # muestra 3 registros
#rows = cursor.fetchall() # muestra todos los registros
#print(rows)
