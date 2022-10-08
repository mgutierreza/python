from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from objConexionBD.consultasBD import obtenerData
from util.utilitario import gestionArchivos

class objetoEntity(iObjetoAplicacion):

    def __init__(self,nombreTabla,claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreClase = ''
        self.TAB = '\t'
        self.ENTER = '\t'

    def generarArchivo(self):
        nuevoArchivo = gestionArchivos(self.__nombreTabla, self.__claseObjeto)
        self.__nombreClase = nuevoArchivo.generarNombreArchivo()
        contenidoClase = self.__generarClase()
        nuevoArchivo.generarArchivo(contenidoClase)
        return

    def __generarClase(self):
        clase = ""
        clase += self.__generarCabeceraClase()
        clase += "namespace EP_AcademicMicroservice.Entities" + self.TAB 
        clase += "{" + self.ENTER
        clase += self.TAB + "[DataContract]" + self.ENTER
        clase += self.TAB + "public class " + self.__nombreClase + self.ENTER 
        clase += self.TAB + "{" + self.ENTER 
        clase += self.__generarCuerpoClase()
        clase += self.TAB + "}" + self.ENTER 
        clase += "}" + self.ENTER
        return clase
 
    def __generarCabeceraClase(self):
        cabeceraClase = ""
        cabeceraClase += "using System;" + self.ENTER
        cabeceraClase += "using System.Collections.Generic;" + self.ENTER
        cabeceraClase += "using System.ComponentModel.DataAnnotations;" + self.ENTER
        cabeceraClase += "using System.Linq;" + self.ENTER 
        cabeceraClase += "using System.Runtime.Serialization;" + self.ENTER 
        cabeceraClase += "using System.Text;" + self.ENTER
        cabeceraClase += "using System.Threading.Tasks;" + 3*self.ENTER
        return cabeceraClase

    def __generarCuerpoClase(self):
        cuerpoClase = ""
        tipoDato = ""
        datamember =  "[DataMember(EmitDefaultValue = false)]"
        textoGetSet = " { get; set; }"
        
        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for clave, valor in dictData.items():
            if (valor == 'INT'):
                tipoDato = "public Int32 "
            elif (valor == 'VARCHAR'):
                tipoDato = "public String "
            else:
                tipoDato = "public DateTime "
            cuerpoClase += 2*self.TAB + datamember + self.ENTER 
            cuerpoClase += 2*self.TAB + tipoDato + dictData[0] + textoGetSet + 2*self.ENTER

        return cuerpoClase
