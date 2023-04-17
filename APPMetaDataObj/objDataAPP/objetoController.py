from objDataAPP.iObjetoAplicacion import iObjetoAplicacion
from util.utilitario import gestionArchivos
from objConexionBD.consultasBD import obtenerData

class objetoRepository(iObjetoAplicacion):

    def __init__(self, nombreTabla, claseObjeto):
        self.__nombreTabla = nombreTabla
        self.__claseObjeto = claseObjeto
        self.__nombreClase = ''
        self.TAB = '\t'
        self.ENTER = '\n'

    def generarArchivo(self):
        nuevoArchivo = gestionArchivos(self.__nombreTabla, self.__claseObjeto)
        self.__nombreClase = nuevoArchivo.generarNombreArchivo()
        contenidoClase = self.__generarClase()
        nuevoArchivo.generarArchivo(contenidoClase)
        return

    def __generarClase(self):
        clase = ""
        clase += self.__generarCabeceraClase()
        clase += "namespace EP_AcademicMicroservice.Api.Controllers" + self.ENTER 
        clase += "{"  + self.ENTER   
        clase += self.TAB + "[Route(\"api/[controller]\")]" + self.ENTER
        clase += self.TAB + "[ApiController]" + self.ENTER
        clase += self.TAB + "public class " + self.__nombreClase + " : ControllerBase" + self.ENTER
        clase += self.TAB + "{" + self.ENTER         
        clase += self.__generarCuerpoClase()    
        clase += self.TAB + "}" + self.ENTER        
        clase += "}"

        return clase
    
    def __generarCabeceraClase(self):
        cabeceraClase = ""
        cabeceraClase += "using EP_AcademicMicroservice.Service;" + self.ENTER 
        cabeceraClase += "using EP_AcademicMicroservice.Entities;" + self.ENTER 
        cabeceraClase += "using Microsoft.AspNetCore.Mvc;" + self.ENTER
        cabeceraClase += "using System;" + self.ENTER 
        cabeceraClase += "using System.Collections.Generic;" + self.ENTER
        cabeceraClase += "using System.Linq;" + self.ENTER
        cabeceraClase += "using System.Threading.Tasks;" + 2*self.ENTER

        return cabeceraClase
    
    def __generarCuerpoClase(self):
        cuerpoClase = ""

        cuerpoClase += 2*self.TAB + "#region Operations" + self.ENTER 
        cuerpoClase += 2*self.TAB + "[HttpGet(\"GetByPagination\", Name = \"" + self.__nombreTabla + "_GetByPagination\")]" + self.ENTER 
        cuerpoClase += 2*self.TAB + "[ProducesResponseType(200)]" + self.ENTER 
        cuerpoClase += 2*self.TAB + "[ProducesResponseType(400)]" + self.ENTER 
        cuerpoClase += self.__generarMetodoObtenerByPagination() + 2*self.ENTER
        cuerpoClase += 2*self.TAB + "[HttpGet(\"{Id}\", Name = \"" + self.__nombreTabla + "_GetById\")]" + self.ENTER 
        cuerpoClase += 2*self.TAB + "[ProducesResponseType(200)]" + self.ENTER 
        cuerpoClase += 2*self.TAB + "[ProducesResponseType(400)]" + self.ENTER
        cuerpoClase += 2*self.TAB + "[ProducesResponseType(404)]" + self.ENTER
        cuerpoClase += self.__generarMetodoObtenerByID() + 2*self.ENTER
        cuerpoClase += 2*self.TAB + "[HttpPost(\"Insert\")]" + self.ENTER
        cuerpoClase += self.__generarMetodoPost() + 2*self.ENTER
        cuerpoClase += 2*self.TAB + "[HttpPost(\"update\")]" + self.ENTER
        cuerpoClase += self.__generarMetodoUpdate() + 2*self.ENTER
        cuerpoClase += 2*self.TAB + "[HttpPost(\"Delete\")]" + self.ENTER
        cuerpoClase += self.__generarMetodoDelete() + 2*self.ENTER
        cuerpoClase += 2*self.TAB + "#endregion" + self.ENTER 
        
        return cuerpoClase

    def __generarMetodoObtenerByPagination(self):
        MetodoObtenerByPagination = ""

        MetodoObtenerByPagination += 2*self.TAB + "public IActionResult GetByPagination()" + self.ENTER
        MetodoObtenerByPagination += 2*self.TAB + "{" + self.ENTER 
        MetodoObtenerByPagination += 3*self.TAB + self.__nombreTabla + "LstItemResponse response = null;" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + self.__nombreTabla + "LstItemRequest request = new " + self.__nombreTabla + "LstItemRequest()" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "{" + self.ENTER
        MetodoObtenerByPagination += 4*self.TAB + "Filter = new " + self.__nombreTabla + "Filter() { }," + self.ENTER
        MetodoObtenerByPagination += 4*self.TAB + "FilterType = " + self.__nombreTabla + "FilterLstItemType.ByPagination" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "};" + 2*self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "try" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "{" + self.ENTER
        MetodoObtenerByPagination += 4*self.TAB + "response = new " + self.__nombreTabla + "Service().GetLst" + self.__nombreTabla + "(request);" + self.ENTER
        MetodoObtenerByPagination += 4*self.TAB + "if (!response.IsSuccess)" + self.ENTER
        MetodoObtenerByPagination += 5*self.TAB + "return BadRequest(response);" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "}" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "catch (Exception)" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "{" + self.ENTER
        MetodoObtenerByPagination += 4*self.TAB + "throw;" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "}" + self.ENTER
        MetodoObtenerByPagination += 3*self.TAB + "return Ok(response);" + self.ENTER
        MetodoObtenerByPagination += 2*self.TAB + "}" + self.ENTER

        return MetodoObtenerByPagination

    def __generarMetodoObtenerByID(self):
        metodoObtenerByID = ""
        tipoDatoClavePrincipal = ""
        nombreCampoClavePrincipal = ""
        tipoDato = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            tipoDatoClavePrincipal = valor["tipoDato"]
            nombreCampoClavePrincipal = valor["nombreCampo"]
        
        if (tipoDatoClavePrincipal == 'INT'):
            tipoDato = "Int32"
        elif (tipoDatoClavePrincipal == 'VARCHAR'):
            tipoDato = "String"
        else:
            tipoDato = "DateTime"

        metodoObtenerByID += 2*self.TAB + "public IActionResult GetById(" + tipoDato + " Id)" + self.ENTER
        metodoObtenerByID += 2*self.TAB + "{" + self.ENTER 
        metodoObtenerByID += 3*self.TAB + self.__nombreTabla + "ItemResponse response = null;" + self.ENTER
        metodoObtenerByID += 3*self.TAB + self.__nombreTabla + "ItemRequest request = new " + self.__nombreTabla + "ItemRequest()" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "{" + self.ENTER
        metodoObtenerByID += 4*self.TAB + "Filter = new " + self.__nombreTabla + "Filter() { " + nombreCampoClavePrincipal + " = Id }," + self.ENTER
        metodoObtenerByID += 4*self.TAB + "FilterType = " + self.__nombreTabla + "FilterItemType.ById" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "};" + 2*self.ENTER
        metodoObtenerByID += 3*self.TAB + "try" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "{" + self.ENTER
        metodoObtenerByID += 4*self.TAB + "response = new " + self.__nombreTabla + "Service().Get" + self.__nombreTabla + "(request);" + self.ENTER
        metodoObtenerByID += 4*self.TAB + "if (!response.IsSuccess)" + self.ENTER
        metodoObtenerByID += 5*self.TAB + "return BadRequest(response);" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "}" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "catch (Exception)" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "{" + self.ENTER
        metodoObtenerByID += 4*self.TAB + "throw;" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "}" + self.ENTER
        metodoObtenerByID += 3*self.TAB + "return Ok(response);" + self.ENTER
        metodoObtenerByID += 2*self.TAB + "}" + self.ENTER

        return metodoObtenerByID

    def __generarMetodoPost(self):
        metodoPost = ""

        metodoPost += 2*self.TAB + "public IActionResult Post([FromBody] " + self.__nombreTabla + "Entity Estructura)" + self.ENTER
        metodoPost += 2*self.TAB + "{" + self.ENTER 
        metodoPost += 3*self.TAB + self.__nombreTabla + "Response response = null;" + self.ENTER
        metodoPost += 3*self.TAB + self.__nombreTabla + "Request request = new " + self.__nombreTabla + "Request()" + self.ENTER
        metodoPost += 3*self.TAB + "{" + self.ENTER
        metodoPost += 4*self.TAB + "Item = Estructura," + self.ENTER
        metodoPost += 4*self.TAB + "Operation = Operation.Add" + self.ENTER
        metodoPost += 3*self.TAB + "};" + 2*self.ENTER
        metodoPost += 3*self.TAB + "try" + self.ENTER
        metodoPost += 3*self.TAB + "{" + self.ENTER
        metodoPost += 4*self.TAB + "response = new " + self.__nombreTabla + "Service().Execute(request);" + self.ENTER
        metodoPost += 4*self.TAB + "if (!response.IsSuccess)" + self.ENTER
        metodoPost += 5*self.TAB + "return BadRequest(response);" + self.ENTER
        metodoPost += 3*self.TAB + "}" + self.ENTER
        metodoPost += 3*self.TAB + "catch (Exception)" + self.ENTER
        metodoPost += 3*self.TAB + "{" + self.ENTER
        metodoPost += 4*self.TAB + "throw;" + self.ENTER
        metodoPost += 3*self.TAB + "}" + self.ENTER
        metodoPost += 3*self.TAB + "return Ok(response);" + self.ENTER
        metodoPost += 2*self.TAB + "}" + self.ENTER

        return metodoPost   

    def __generarMetodoUpdate(self):
        metodoUpdate = ""

        metodoUpdate += 2*self.TAB + "public IActionResult Put([FromBody] " + self.__nombreTabla + "Entity Estructura)" + self.ENTER
        metodoUpdate += 2*self.TAB + "{" + self.ENTER 
        metodoUpdate += 3*self.TAB + self.__nombreTabla + "Response response = null;" + self.ENTER
        metodoUpdate += 3*self.TAB + self.__nombreTabla + "Request request = new " + self.__nombreTabla + "Request()" + self.ENTER
        metodoUpdate += 3*self.TAB + "{" + self.ENTER
        metodoUpdate += 4*self.TAB + "Item = Estructura," + self.ENTER
        metodoUpdate += 4*self.TAB + "Operation = Operation.Edit" + self.ENTER
        metodoUpdate += 3*self.TAB + "};" + 2*self.ENTER
        metodoUpdate += 3*self.TAB + "try" + self.ENTER
        metodoUpdate += 3*self.TAB + "{" + self.ENTER
        metodoUpdate += 4*self.TAB + "response = new " + self.__nombreTabla + "Service().Execute(request);" + self.ENTER
        metodoUpdate += 4*self.TAB + "if (!response.IsSuccess)" + self.ENTER
        metodoUpdate += 5*self.TAB + "return BadRequest(response);" + self.ENTER
        metodoUpdate += 3*self.TAB + "}" + self.ENTER
        metodoUpdate += 3*self.TAB + "catch (Exception)" + self.ENTER
        metodoUpdate += 3*self.TAB + "{" + self.ENTER
        metodoUpdate += 4*self.TAB + "throw;" + self.ENTER
        metodoUpdate += 3*self.TAB + "}" + self.ENTER
        metodoUpdate += 3*self.TAB + "return Ok(response);" + self.ENTER
        metodoUpdate += 2*self.TAB + "}" + self.ENTER

        return metodoUpdate  
    
    def __generarMetodoDelete(self):
        metodoDelete = ""
        tipoDatoClavePrincipal = ""
        nombreCampoClavePrincipal = ""
        tipoDato = ""

        data = obtenerData(self.__nombreTabla)
        dictData = data.metaDataClavePrincipal()

        for valor in dictData:
            tipoDatoClavePrincipal = valor["tipoDato"]
            nombreCampoClavePrincipal = valor["nombreCampo"]
        
        if (tipoDatoClavePrincipal == 'INT'):
            tipoDato = "Int32"
        elif (tipoDatoClavePrincipal == 'VARCHAR'):
            tipoDato = "String"
        else:
            tipoDato = "DateTime"

        metodoDelete += 2*self.TAB + "public IActionResult Delete(" + tipoDato + " Id)" + self.ENTER
        metodoDelete += 2*self.TAB + "{" + self.ENTER 
        metodoDelete += 3*self.TAB + self.__nombreTabla + "Response response = null;" + self.ENTER
        metodoDelete += 3*self.TAB + self.__nombreTabla + "Request request = new " + self.__nombreTabla + "Request()" + self.ENTER
        metodoDelete += 3*self.TAB + "{" + self.ENTER
        metodoDelete += 4*self.TAB + "Item = new " + self.__nombreTabla + "Entity() { " + nombreCampoClavePrincipal + " = Id }," + self.ENTER
        metodoDelete += 4*self.TAB + "Operation = Operation.Delete" + self.ENTER
        metodoDelete += 3*self.TAB + "};" + 2*self.ENTER
        metodoDelete += 3*self.TAB + "try" + self.ENTER
        metodoDelete += 3*self.TAB + "{" + self.ENTER
        metodoDelete += 4*self.TAB + "response = new " + self.__nombreTabla + "Service().Execute(request);" + self.ENTER
        metodoDelete += 4*self.TAB + "if (!response.IsSuccess)" + self.ENTER
        metodoDelete += 5*self.TAB + "return BadRequest(response);" + self.ENTER
        metodoDelete += 3*self.TAB + "}" + self.ENTER
        metodoDelete += 3*self.TAB + "catch (Exception)" + self.ENTER
        metodoDelete += 3*self.TAB + "{" + self.ENTER
        metodoDelete += 4*self.TAB + "throw;" + self.ENTER
        metodoDelete += 3*self.TAB + "}" + self.ENTER
        metodoDelete += 3*self.TAB + "return Ok(response);" + self.ENTER
        metodoDelete += 2*self.TAB + "}" + self.ENTER
        
        return metodoDelete
