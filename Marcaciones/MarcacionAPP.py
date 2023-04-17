import cx_Oracle
import pandas as pd

#connection = cx_Oracle.connect(user="UC_MGUTIERREZA",password="Js8c11Dk",dsn="172.17.23.42:1531/bdpr11g4")
conexion = cx_Oracle.connect(user="UM_MGUTIERREZ",password="R4354%&$t",dsn="172.17.23.9:1530/bdqa11g4")
cursor = conexion.cursor()
print("Successfully connected to Oracle Database")
#cursor = connection.cursor()

archivo_excel = pd.read_excel('d:/marcacion/Registro de asistencias del 10 de abril de 2023.xlsx')
print(archivo_excel.columns)

#values = archivo_excel['Integrante'].values
#print(values)
espacio = ' '
enter = "\n"
textoinicial = '099'
textofijo = '1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127'

columnas = ['Tipo de Modalidad', 'Creado', 'Integrante']
df_seleccionados = archivo_excel[columnas]
modalidades = df_seleccionados.columns[0]
marcas = df_seleccionados.columns[1]
usuarios = df_seleccionados.columns[2]

def getCodigoCarnet(usuario):
    codigoCarnet = '&&&&&'

    script = "SELECT ci.codigocarnet "
    script += "FROM sgcoresys.personamast pe "
    script += "INNER JOIN sgcoresys.as_carnetidentificacion ci ON pe.persona = ci.empleado "
    script += "WHERE pe.codigousuario = \'" + usuario + "\'"
    df = pd.read_sql(script,conexion)

    for i in df.index:
        codigoCarnet = df["CODIGOCARNET"][i]

    return codigoCarnet

f = open('d:/marcacion/archivoBCK_10_04_23.bck','w')

marcaBCK = ''

for index, row in df_seleccionados.iterrows():
    usuario = str(row[usuarios]).strip().replace("@onp.gob.pe","").upper()
    modalidad = str(row[modalidades]).strip().upper()
    marcaFecha = str(row[marcas]).strip()[0:10].replace("-",espacio)
    marcaHora = str(row[marcas]).strip()[11:50].replace(":",espacio)

    if (modalidad == 'PRESENCIAL'):
        modalidad = 'PR'
    elif(modalidad == 'MIXTO REMOTO'):
        modalidad = 'MR'
    elif(modalidad == 'REMOTO'):
        modalidad = 'RE'
    elif(modalidad == 'MIXTO PRESENCIAL'):
        modalidad = 'MP'        
    elif(modalidad == 'TELETRABAJO MIXTO REMOTO'):
        modalidad = 'TR'        
    elif(modalidad == 'TELETRABAJO MIXTO PRESENCIAL'):
        modalidad = 'TP'        
    elif(modalidad == 'TELETRABAJO TOTAL'):
        modalidad = 'TT'
    else:
        modalidad = '&&'
    
    codigoCarnet =  getCodigoCarnet(usuario)
    if (codigoCarnet != '&&&&&'):
        marcaBCK += textoinicial + espacio + marcaFecha + espacio + marcaHora + espacio + textofijo + espacio + codigoCarnet + espacio + modalidad + enter
    
f.write(marcaBCK)
    #print(marcaBCK)
f.close
print('fin de proceso')



