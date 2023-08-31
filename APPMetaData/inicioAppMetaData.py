from obtenerObjetosBD import *
from obtenerObjetosAPP import *
from obtenerJSON import *
from obtenerConexionBD import consultaDatos

#nombreTablaBaseDatos = "UTL_TipNotificacion"
#nombreTablaBaseDatos = "UTL_ClaNotificacion"
#nombreTablaBaseDatos = "UTL_Notificacion"
#nombreTablaBaseDatos = "UTL_NotProgramacion"
#nombreTablaBaseDatos = "UTL_NotProAlcAmplio"



ListaTablas = ['Ven_AccAsiento','Ven_AccDetalle','Ven_AcdVenReferencia','Ven_Comprobante','Ven_ComSunat','Ven_ComSunatBaja','Ven_ComSunatBajaDetail',
                'Ven_ComSunatTicket','Ven_ComSunResLine','Ven_ComSunResumen','Ven_CuoDetail','Ven_CuoHead','Ven_EmiNot','Ven_Head','Ven_HeaDetail',
                'Ven_HeaDetReferenciaItem','Ven_HeaDetRefPayItem','Ven_PayDetail','Ven_PayExtorno','Ven_Payment','Ven_PayReferencia','Ven_PenSunat',
                'Ven_Proceso','Ven_ProDetail','Ven_TicketResponse']

                
#ListaTablas = ['Ven_ProDetail']

for tabla in ListaTablas:
    
    print('Objetos de BD => ' + tabla)

    consultaDatos.establecerNombreTabla(tabla)

    #Creación de Objetos de Base de Datos
    #generarProcedimientoAlmacenadoSelect(tabla)
    #generarProcedimientoAlmacenadoInsercion(tabla)
    generarProcedimientoAlmacenadoActualizacion(tabla)
    #generarProcedimientoAlmacenadoBorrado(tabla)

''' 
    print('Objetos de APP => ' + tabla)cls


    #Creación de Objetos de Aplicación
    generarArchivoEntity(tabla)
    generarArchivoException(tabla)
    generarArchivoFilter(tabla)
    generarArchivoFilterType(tabla)
    generarArchivoRequest(tabla)
    generarArchivoRequestValidator(tabla)
    generarArchivoResponse(tabla)
    generarArchivoRepository(tabla)
    generarArchivoIRepository(tabla)
    generarArchivoService(tabla)
    generarArchivoDomain(tabla)
    generarArchivoController(tabla)

'''
''' 
nombreTablaBaseDatos = "Ven_AccAsiento"


Ven_AccAsiento
Ven_AccDetalle
Ven_AcdVenReferencia
Ven_Comprobante
Ven_ComSunat
Ven_ComSunatBaja
Ven_ComSunatBajaDetail
Ven_ComSunatTicket
Ven_ComSunResLine
Ven_ComSunResumen
Ven_CuoDetail
Ven_CuoHead
Ven_EmiNot
Ven_Head
Ven_HeaDetail
Ven_HeaDetReferenciaItem
Ven_HeaDetRefPayItem
Ven_PayDetail
Ven_PayExtorno
Ven_Payment
Ven_PayReferencia
Ven_PenSunat
Ven_Proceso
Ven_ProDetail
Ven_TicketResponse


#Creación de Objetos de Base de Datos
generarProcedimientoAlmacenadoSelect(nombreTablaBaseDatos)
generarProcedimientoAlmacenadoInsercion(nombreTablaBaseDatos)
generarProcedimientoAlmacenadoActualizacion(nombreTablaBaseDatos)
generarProcedimientoAlmacenadoBorrado(nombreTablaBaseDatos)

#Creación de Objetos de Aplicación
generarArchivoEntity(nombreTablaBaseDatos)
generarArchivoException(nombreTablaBaseDatos)
generarArchivoFilter(nombreTablaBaseDatos)
generarArchivoFilterType(nombreTablaBaseDatos)
generarArchivoRequest(nombreTablaBaseDatos)
generarArchivoRequestValidator(nombreTablaBaseDatos)
generarArchivoResponse(nombreTablaBaseDatos)
generarArchivoRepository(nombreTablaBaseDatos)
generarArchivoIRepository(nombreTablaBaseDatos)
generarArchivoService(nombreTablaBaseDatos)
generarArchivoDomain(nombreTablaBaseDatos)
generarArchivoController(nombreTablaBaseDatos)
'''
#Creación de JSON
#generarJSONInsercion(nombreTablaBaseDatos)