import cx_Oracle
import pandas as pd
from manageBD import getCarnetIdentificacion

dataCarnetIdentificacion = []

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

def getDataArchivoExcel():
    archivo_excel = pd.read_excel('d:/marcacion/Registro_asistencias_16_04_2023.xlsx')
    columnas = ['Tipo de Modalidad', 'Creado', 'Integrante']
    df_seleccionados = archivo_excel[columnas]
    return df_seleccionados

def getArchivoBCK():
    df_seleccionados = getDataArchivoExcel()
    modalidades = df_seleccionados.columns[0]
    marcas = df_seleccionados.columns[1]
    usuarios = df_seleccionados.columns[2]

    espacio = ' '
    enter = "\n"
    textoinicial = '099'
    textofijo = '1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127'

    f = open('d:/marcacion/archivoBCK_16_04_23.bck','w')

    marcaBCK = ''

    for index, row in df_seleccionados.iterrows():
        usuario = str(row[usuarios]).strip().replace("@onp.gob.pe","").upper()
        modalidad = str(row[modalidades]).strip().upper()
        marcaFecha = str(row[marcas]).strip()[0:10].replace("-",espacio)
        marcaHora = str(row[marcas]).strip()[11:50].replace(":",espacio)

        codigoModalidad = getModalidad(modalidad)
        carnetIdentificacion =  getCarnetIdentificacion(usuario)

        if (carnetIdentificacion != '&&&&&' and codigoModalidad != '&&'):
            marcaBCK += textoinicial + espacio + marcaFecha + espacio + marcaHora + espacio + textofijo + espacio + carnetIdentificacion + espacio + codigoModalidad + enter
        
    f.write(marcaBCK)
    f.close
    print('fin de proceso')

    return

getArchivoBCK()

#cursor.execute("SELECT * FROM sgcoresys.as_carnetidentificacion WHERE estado = \'I\'")
#rows = cursor.fetchone() # muestra un registro
#rows = cursor.fetchmany(3) # muestra 3 registros
#rows = cursor.fetchall() # muestra todos los registros
#print(rows)
