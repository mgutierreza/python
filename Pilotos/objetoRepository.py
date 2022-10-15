from consultasBD import obtenerData
from utilitario import gestionArchivos

class objetoRepository():

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreClase = ''
        self.TAB = '\t'
        self.ENTER = '\n'
        self.__generarCamposInsertar()

    def __generarCamposInsertar(self):
        campoInsertar = ""
        tipoDato = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataTodosCampos()

        numeroCampos = len(dictData)
        x = numeroCampos - 4
        y = numeroCampos - 5
        z = numeroCampos - 6

        #print(dictData[z])
        #print(dictData[y])
        #print(dictData[x])
        dictData.pop(x)
        dictData.pop(y)
        dictData.pop(z)
       
        for valor in dictData:
            if (valor["tipoDato"] == 'INT'):
                tipoDato = "DbType.Int32"
            elif (valor["tipoDato"] == 'VARCHAR'):
                tipoDato = "DbType.String"
            else:
                tipoDato = "DbType.DateTime"

            if (valor["tipoCampo"] == 'PRIMARY KEY'):
                campoInsertar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] 
                campoInsertar += ", " + tipoDato + ", direction: ParameterDirection.Output); " + self.ENTER
            else:
                campoInsertar += 3*self.TAB + "param.Add(@" + valor["nombreCampo"] + ", item." + valor["nombreCampo"] 
                campoInsertar += ", " + tipoDato + "); " + self.ENTER

        return print(campoInsertar)

