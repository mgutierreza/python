import pyodbc as pyo

class gestionBaseDatos():

    def __init__(self, nombreTabla):
        self.__nombreTabla = nombreTabla
        self.driver = ''
        self.server = ''
        self.database = ''
        self.user = ''
        self.password = ''
        self.conexionBD = None

    def consultarDatosBD(self, consulta):

        conexion = self.__obtenerConexionBD()
        cursor = conexion.cursor()
        #cursor = conexion.cursor(dictionary = True)
        #cursor.execute(consulta, self.__nombreTabla)
        cursor.execute(consulta)
        filas = cursor.fetchall()
        registros = []
        columnas = [column[0] for column in cursor.description]
                
        for fila in filas:
            registros.append(dict(zip(columnas, fila)))
        
        cursor.close()
        self.__cerrarConexionBD()
    
        return registros

    def __obtenerConexionBD(self):

        if (self.conexionBD == None):
            self.conexionBD = self.__conectarBD()

        return self.conexionBD
    
    def __conectarBD(self):

        conexionAzure = (
            r"Driver={SQL SERVER};Server=tcp:developerep.database.windows.net;Database=BDEpartners_Dev;UID=epartners;PWD=Peam41923m*"
        )
        self.conexionBD = pyo.connect(conexionAzure)

        return self.conexionBD
    
    def __cerrarConexionBD(self):

        if (self.conexionBD != None):
            self.conexionBD.close()

        return
